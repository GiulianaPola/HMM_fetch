#!/usr/bin/env python3
import argparse
import sys
import os
from datetime import datetime

version='1.0.3'

param=dict()
hmms=[]
start_time = datetime.now()
call=os.path.abspath(os.getcwd())

help = 'hmm_fetch v{} - \n'.format(version)
help += '(c) 2022. Arthur Gruber & Giuliana Pola\n'
help = help + 'For more information access https://github.com/GiulianaPola/HMM_fetch\n'
help += 'Usage: hmm_fetch.py -i <list file> -d <hmm file>\n'
help += '\nMandatory parameters:\n'
help += '-i <text file>\tProfile HMM name list\n'
help += '-d <hmm file>\tProfile HMM dataset\n'
help += '\nOptional parameters:\n'
help += '-o <name>\tOutput directory name (default: hmm_selected)'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-i')
parser.add_argument('-d')
parser.add_argument('-o')
parser.add_argument('-version', action='store_true')
parser.add_argument('-h', '--help', action='store_true')
args = parser.parse_args()

def rename(i,name,typ):
  path=''
  if '/' in name:
    path=os.path.split(name)[0]
    name=os.path.split(name)[1]
  newname=os.path.join(path, name)
  if typ=='dir':
    while os.path.isdir(newname):
      i+=1
      newname=os.path.join(path, str(name+str(i)))
  elif typ=='file':
    while os.path.isfile(newname):
      i+=1
      newname=os.path.join(path, str(name+str(i)))

  return newname

def validate_args(args):
  valid=True
  
  if args.i==None:
    print("Missing profile HMM name list (-i)!")
    valid=False
  elif not args.i==None:
   if not os.path.isfile(args.i):
     print("Profile HMM name list (-i) not exist!")
     valid=False
   else:
     param["i"]=os.path.realpath(args.i)
   
  if args.d==None:
    print("Missing profile HMM dataset (-d)!")
    valid=False
  elif not args.d==None:
    if not os.path.isfile(args.d):
      print("Profile HMM dataset (-d) does not exist!")
      valid=False
    else:
      param["d"]=os.path.realpath(args.d)
  
  if valid==True:
    if args.o==None:
      out=os.path.join(call,'hmm_selected')
    else:
      head_tail = os.path.split(args.o)
      if os.path.exists(head_tail[0]):
        out=args.o
      else:
        out=os.path.join(call,head_tail[1])
    if os.path.isdir(args.o):
      print("Output directory '{}' already exist!".format(out))
      out=rename(1,out,'dir')
    try:
      os.mkdir(out)
    except:
      print("Output directory '{}' couldn't be created!".format(out))
      valid=False
    else:
      print("Creating output directory '{}'...".format(out))
      param['o']=out

  return valid,param

def validate_list(i):
  valid=True
  namelist=[]
  itext=''
  try:
    ifile=open(i,"r")
  except:
    print("Profile HMM name list (-i) couldn't be opened!")
    valid=False
  else:
    itext=ifile.read()
    if itext.isspace() or len(itext)==0:
      print("Profile HMM name list (-i) is empty!")
      valid=False
    else:
      if '\n' in itext:
        namelist=itext.split('\n')
      elif '\t' in itext:
        namelist=itext.split('\t')
      elif ';' in itext:
        namelist=itext.split(';')
      elif ',' in itext:
        namelist=itext.split(',')
      elif ' ' in itext:
        namelist=itext.split(' ')
      while '' in namelist:
        namelist.remove('')
  return valid,sorted(namelist)
  
def validate_database(d):
  valid=True
  database=''
  dtext=''
  try:
    dfile=open(d,"r")
  except:
    print("Profile HMM dataset (-d) couldn't be opened!")
    valid=False
  else:
    dtext=dfile.read()
    if dtext.isspace() or len(dtext)==0:
      print("Profile HMM dataset (-d) is empty!")
      valid=False
    else:
      database=dtext
      
  return valid,database

if not len(sys.argv)>1:
    print(help)
elif args.help == True:
    print(help)
elif args.version == True:
    print(version)
else:
  valid,param=validate_args(args)
  if valid==True:
    print("Valid arguments!")
    try:
      flog=open(os.path.join(param["o"], 'file.flog'),'w')
      flog.write('hmm_fetch v{}\n'.format(version))
      flog.write('\nWorking directory:\n{}\n'.format(call))
      flog.write('\nCommand line:\n{}\n'.format(' '.join(sys.argv)))
      flog.write('\nParameters:\n{}\n'.format(str(param)))
      flog.write('\nDataset analysis:\n')
    except:
      print('flog file was not created!')
    else:  
      valid,namelist=validate_list(param['i'])
      if valid==True:
        valid,database=validate_database(param['d'])
        if valid==True:
          missing=[]
          selected=[]
          for name in namelist:
            if name not in database:
              missing.append(name)
            else:
              selected.append(name)
              head=database.split("NAME  "+name)[0]
              tail=database.split("NAME  "+name)[1]
              hmm="HMMER"+head.split("HMMER")[-1]+"NAME  "+name+tail.split("//")[0]+"//"
              hmms.append(hmm)
              with open(os.path.join(param['o'], '{}.hmm'.format(name)),'w') as hmmfile:
                hmmfile.write(hmm)
          if not selected==[]:
            flog.write("Selected HMMs: {}\n".format(selected))
          if not missing==[]:
            flog.write("Missing HMMs: {}\n".format(missing))
          execution=datetime.now() - start_time
          print("\nExecution time: {}".format(execution))
          flog.write("\nExecution time: {}".format(execution))
          print("Number of selected files: {}".format(len(selected)))
          flog.write("\nNumber of selected files: {}".format(len(selected)))
          if selected==[]:
            print("All selected HMMs are missing!")
            flog.write("\nAll selected HMMs are missing!\n")
          else:
            with open(os.path.join(param['o'], 'selected.hmm'),'w') as selectedfile:
              selectedfile.write('\n'.join(hmms))
            if missing==[]:
              print("All selected HMMs were saved!")
              flog.write("\nAll selected HMMs were saved!\n")
            else:
              print("Missing HMMs:\t{}\n".format(missing.join(',')))
              flog.write("\nMissing HMMs:\t{}\n".format(missing.join(',')))
              print("Selected HMMs:\t{}\n".format(selected.join(',')))
              flog.write("Selected HMMs:\t{}\n".format(selected.join(',')))
            print("Execution time per file: {}".format(execution/len(selected)))
            flog.write("Execution time per file: {}".format(execution/len(selected)))
      flog.close()
print("Done.")      