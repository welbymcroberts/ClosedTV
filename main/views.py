# Create your views here.
from django.http import HttpResponseRedirect
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


def index(request):
    areas = Area.objects.all()
    return render_to_response('index.html',{'areas': areas})
def regions(request,area):
    area = get_object_or_404(Area,pk=area)
    r = area.region_set.values()
    return render_to_response('regions.html',{'r': r})

def channels(request,region):
    area = get_object_or_404(Area,Q(region=region))
    r6 = get_object_or_404(Region,Q(area=area) & Q(regionid=65535))
    regions = get_list_or_404(Region,Q(pk=region) | Q(pk=r6.pk))
    c = []
    for region in regions:
        c += region.channel_set.values()
    return render_to_response('channels.html',{'c': c, 'r': region})

def generate(request):
    region = request.REQUEST['region']
    sourceid = request.REQUEST['sourceid']
    sourcename = request.REQUEST['sourcename']
    headendid = '{'+request.REQUEST['headendid']+'}'
    area = get_object_or_404(Area,Q(region=region))
    r6 = get_object_or_404(Region,Q(area=area) & Q(regionid=65535))
    regions = get_list_or_404(Region,Q(pk=region) | Q(pk=r6.pk))
    c = []
    for region in regions:
        c += get_list_or_404(Channel,region=region)
    res = render_to_response('dvb.html',{'c': c, 'sourceid': sourceid, 'sourcename': sourcename, 'headendid': headendid, }, mimetype='application/xml')
    #res['Content-Disposition'] = "attachment; filename=DVBChannelSync.xml";
    return res

def update_xml(request):
            Area.objects.all().delete()
            Region.objects.all().delete()
            Channel.objects.all().delete()
            ScannedChannel.objects.all().delete()
            areaxml = et.parse(BASE_DIR+'xml/AreaRegionChannelInfo.xml').getroot()
            for area in areaxml.findall('area'):
               # Create the areas
               print('new area')
               a = Area(id=area.attrib['id'],name=area.attrib['name'])
               a.save()
               for region in area.findall('region'):
                  r = Region(area=a,regionid=region.attrib['id'])
                  r.save()
                  for channel in region.findall('channel'):
                      c = Channel(region=r,number=channel.attrib['id'],nid=channel.attrib['nid'],tid=channel.attrib['tid'],sid=channel.attrib['sid'],name=channel.attrib['name'])
                      c.save()
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
                           pp(sc)
                           sc.save()

    



            return HttpResponseRedirect('/done')
