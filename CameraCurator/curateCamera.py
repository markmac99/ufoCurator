# curateCamera.py
#
# python script to validate data before uploading to ukon live
#

import os
import fnmatch
import shutil
import glob

import configparser as cfg

from CameraCurator import curateEngine as ce


def valid_date(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    if len(s) == 8:
        return True
    return False


def AddToRemoveList(fname, movebad=False, msg='', nobjs=0, maxbri=0, tottotpx=0, useSubfolders=False, badfilepath='.', log=None):
    _, fn = os.path.split(fname)
    namelen = len(fname)
    allf = fname[:namelen - 4] + '*'
    if movebad is True:
        bfp = badfilepath
        if useSubfolders is True:
            typ = msg.split(',')[0]
            bfp = os.path.join(badfilepath, typ)
            if os.path.exists(bfp) is False:
                os.mkdir(bfp)
        for fl in glob.glob(allf):
            _, fna = os.path.split(fl)
            trg = os.path.join(bfp, fna)
            if os.path.exists(trg):
                os.remove(trg)
            shutil.move(fl, trg)
    else:
        pass
    msg = msg + ',{:d},{:d}, {:d}'.format(nobjs, int(maxbri), int(tottotpx))
    log.info(fn + ',' + msg)


def ProcessADay(path, ymd, badfilepath, logfilepath, movebad, useSubfolders, log=None):

    try:
        listOfFiles = os.listdir(path)
    except:
        if log is not None:
            log.info('nothing to analyse')
        return
    listOfFiles.sort()
    pattern = 'M{:s}*P.jpg'.format(ymd)
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            x = entry.find('UK00')
            if x == -1:
                jpgname = os.path.join(path, entry)
                xmlname = jpgname[:len(jpgname) - 5] + ".xml"
                sts, msg, nobjs, maxbri, gtp, tottotpx = ce.CheckifValidMeteor(xmlname, log)
                if sts is False:
                    AddToRemoveList(xmlname, movebad, msg, nobjs, maxbri, tottotpx, useSubfolders, badfilepath, log)
                else:
                    msg = msg + ',{:d},{:d}, {:d}'.format(nobjs, int(maxbri), int(tottotpx))
                    _, fn = os.path.split(xmlname)
    return


def main(infname, ymd):
    if valid_date(ymd) is True:
        config = cfg.ConfigParser()
        config.read(infname)
        srcpath = config['camera']['localfolder']
        badfilepath = config['cleaning']['badfolder']
        logfilepath = badfilepath
        ce.logname = 'Curator: '
        ce.MAXRMS = float(config['cleaning']['maxrms'])
        ce.MINLEN = int(config['cleaning']['minlen'])
        ce.MAXLEN = int(config['cleaning']['maxlen'])
        ce.MAXBRI = int(config['cleaning']['maxbri'])
        ce.MAXOBJS = int(config['cleaning']['maxobjs'])

        if config['cleaning']['debug'] in ['True', 'TRUE', 'true']:
            ce.debug = True
        else:
            ce.debug = False
        movebad = False
        if config['cleaning']['movefiles'] in ['True', 'TRUE', 'true']:
            movebad = True
        useSubfolders = False
        if config['cleaning']['useSubfolders'] in ['True', 'TRUE', 'true']:
            useSubfolders = True  # noqa: F841

        yyyy = ymd[:4]
        yymm = ymd[:6]
        path = os.path.join(srcpath, yyyy, yymm, ymd)
        try:
            os.mkdir(badfilepath)
        except:
            pass
        try:
            os.mkdir(logfilepath)
        except:
            pass
        ProcessADay(path, ymd, badfilepath, logfilepath, movebad, useSubfolders)
    else:
        print('Invalid date, must be YYYYMMDD')
