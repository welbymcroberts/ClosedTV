# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from copy import copy
import itertools
import xml.etree.cElementTree as et
from pprint import pprint as pp
from main.models import *
from django.conf import settings 
from django.db.models import Q

if settings.BASE_DIR:
    BASE_DIR = settings.BASE_DIR


def tv_or_radio(ch_list,radio=False):
    c = []
    for ch in ch_list:
        if ch['number'] > 100 and ch['number'] < 1000:
            #These are TV Channels
            c +=  [ch]
        if ch['number'] > 3000 and ch['number'] < 4000:
            #These are Radio Channels
            if radio:
                c += [ch]
    return c

def index(request):
    areas = Area.objects.all()
    return render_to_response('index.html',{'areas': areas})

def regions(request,area):
    area = get_object_or_404(Area,pk=area)
    r = area.region_set.extra("SELECT main_channel.name FROM main_channel WHERE main_channel.number = 101 AND main_channel.region_id = main_region.id").extra("SELECT main_channel.name FROM main_channel WHERE main_channel.number = 103 AND main_channel.region_id = main_region.id").values()
    return render_to_response('regions.html',{'r': r})

def channels(request,region):
    area = get_object_or_404(Area,Q(region=region))
    r6 = get_object_or_404(Region,Q(area=area) & Q(regionid=65535))
    regions = get_list_or_404(Region,Q(pk=region) | Q(pk=r6.pk))
    c = []
    for reg in regions:
        c += tv_or_radio(reg.channel_set.values())
    return render_to_response('channels.html',{'c': sorted(c, key=lambda epgid: epgid['number'] ), 'r': Region.objects.get(pk=region)})

def generate_list(request,region,radio):
    if request.REQUEST['fta'] == 'fta':
        fta = (Q(fta=0))
    else:
        fta = (Q(fta=0) | Q(fta=1))
    area = get_object_or_404(Area,Q(region=region))
    r6 = get_object_or_404(Region,Q(area=area) & Q(regionid=65535))
    regions = get_list_or_404(Region,Q(pk=region) | Q(pk=r6.pk))
    c = []
    for region in regions:
        c += tv_or_radio(region.channel_set.filter(fta).values(),radio)
    return c
def headend(h,version=3):
    print version
    if version == "4":
        headendid = h
    else:
        headendid = '{'+h+'}'
    return headendid
def get_parms(request,number=1,version=3):
    sourceid = request.REQUEST['sourceid'+str(number)]
    sourcename = request.REQUEST['sourcename'+str(number)]
    headendid = headend(request.REQUEST['headendid'+str(number)],version)
    print headendid
    return (sourceid,sourcename,headendid)
def generate(request):
    region = request.REQUEST['region']
    no_tuners = int(request.REQUEST['tuners'])
    version = request.REQUEST['version']
    sourceid={}
    sourcename={}
    headendid={}
    tuners = []
    if request.REQUEST['radio'] == 1:
        radio = True
    else:
        radio = False
    if no_tuners > 0:
        (sourceid[1],sourcename[1],headendid[1]) = get_parms(request,1,version)
	tuners.append({'sourceid':sourceid[1],'sourcename':sourcename[1],'headendid':headendid[1]})
    if no_tuners > 1:
        (sourceid[2],sourcename[2],headendid[2]) = get_parms(request,2,version)
	tuners.append({'sourceid':sourceid[2],'sourcename':sourcename[2],'headendid':headendid[2]})
    if no_tuners > 2:
        (sourceid[3],sourcename[3],headendid[3]) = get_parms(request,3,version)
	tuners.append({'sourceid':sourceid[3],'sourcename':sourcename[3],'headendid':headendid[3]})
    if no_tuners > 3:
        (sourceid[4],sourcename[4],headendid[4]) = get_parms(request,4,version)
	tuners.append({'sourceid':sourceid[4],'sourcename':sourcename[4],'headendid':headendid[4]})
    if no_tuners > 4:
        (sourceid[5],sourcename[5],headendid[5]) = get_parms(request,5,version)
        tuners.append({'sourceid':sourceid[5],'sourcename':sourcename[5],'headendid':headendid[5]})
    if no_tuners > 5:
        (sourceid[6],sourcename[6],headendid[6]) = get_parms(request,6,version)
        tuners.append({'sourceid':sourceid[6],'sourcename':sourcename[6],'headendid':headendid[6]})
    if no_tuners > 6:
        (sourceid[7],sourcename[7],headendid[7]) = get_parms(request,7,version)
        tuners.append({'sourceid':sourceid[7],'sourcename':sourcename[7],'headendid':headendid[7]})
    if no_tuners > 7:
        (sourceid[8],sourcename[8],headendid[8]) = get_parms(request,8,version)
        tuners.append({'sourceid':sourceid[8],'sourcename':sourcename[8],'headendid':headendid[8]})
    c = generate_list(request,region,radio)
    from pprint import pprint as pp
    tuner1 = { 'sourceid': sourceid[1], 'sourcename': sourcename[1], 'headendid': headendid[1] }
    res = render_to_response('dvb.html',{'c': sorted(c, key=lambda epgid: epgid['number'] ), 'sourceid': sourceid[1], 'sourcename': sourcename[1], 'headendid': headendid[1], 'tuners': tuners } , mimetype='application/xml')
    if version == 4:
        res['Content-Disposition'] = "attachment; filename=DVBLink_ChannelStorage.xml";
    else
        res['Content-Disposition'] = "attachment; filename=DVBLinkChannelStorage.xml";
    return res

def update_xml(request):
            Area.objects.all().delete()
            Region.objects.all().delete()
            Channel.objects.all().delete()
            ScannedChannel.objects.all().delete()


            scanned = {}
            tvsourcexml = et.parse(BASE_DIR+'xml/TVSourceSettings.xml').getroot()
            for Channels in tvsourcexml.findall('Channels'):
                for Headend in Channels.findall('Headend'):
                    for ChannelList in Headend.findall('ChannelList'):
                       for c in ChannelList.findall('Channel'):
                           sc = ScannedChannel(fec=c.find('Fec').text,
                            diseqc=c.find('Diseqc').text,
                            diseqcrawdata='0', #c.find('DiseqcRawData').text,
                            freq=c.find('Freq').text,
                            lnbsel = c.find('LNBSel').text,
                            lof = c.find('LOF').text,
                            mod = c.find('Mod').text,
                            sr = c.find('SR').text,
                            pol = c.find('Pol').text,
                            nid = c.find('nid').text,
                            tid = c.find('tid').text,
                            sid = c.find('sid').text,
                            encrypt = c.find('Encrypt').text,
                            type = c.find('Type').text,
                            chnum = c.find('ChNum').text,
                            chsubnum = c.find('ChSubNum').text,
                            ecm_pid = c.find('ecm_pid').text,
                            lof1 = c.find('LOF1').text,
                            lof2 = c.find('LOF2').text,
                            lofsw = c.find('LOFSW').text,
                            name = c.find('Name').text,
                            provider = c.find('Provider').text,
                           )
                           sc.save()
                           scanned[sc.nid+':'+sc.tid+':'+sc.sid] = sc 
            areaxml = et.parse(BASE_DIR+'xml/AreaRegionChannelInfo.xml').getroot()
            ret = ''
            for area in areaxml.findall('area'):
               a = Area(id=area.attrib['id'],name=area.attrib['name'])
               a.save()
               for region in area.findall('region'):
                  r = Region(area=a,regionid=region.attrib['id'])
                  r.save()
                  for channel in region.findall('channel'):
                      try:
                          realfrequency = scanned[channel.attrib['nid']+':'+channel.attrib['tid']+':'+channel.attrib['sid']].freq
                          encrypt = scanned[channel.attrib['nid']+':'+channel.attrib['tid']+':'+channel.attrib['sid']].encrypt
                          c = Channel(region=r,number=channel.attrib['id'],nid=channel.attrib['nid'],tid=channel.attrib['tid'],sid=channel.attrib['sid'],name=channel.attrib['name'], realfreq=realfrequency, fta=encrypt)
                          c.save()
                      except:
                          ret +=  "<br />No Scanned Channel for " + channel.attrib['name'] + '  ' + channel.attrib['tid'] + ":" + channel.attrib['sid'] + " in area " + area.attrib['name'] 
            return HttpResponse(ret+'<br /><a href="/">Home</a>')
