#!/usr/bin/env python3
import argparse
import sys
import os
from datetime import datetime

version='1.0.0'

param=dict()
hmms=[]
start_time = datetime.now()
call=os.path.abspath(os.getcwd())

help = 'hmm_fetch v{} - \n'.format(version)
help += '(c) 2022. Arthur Gruber & Giuliana Pola\n'
#help = help + 'For the latest version acess: https://github.com/GiulianaPola/hmm_fetch\n'
help += 'Usage: hmm_fetch.py -i <list file> -d <hmm file>\n'
help += '\nMandatory parameters:\n'
help += '-i <text file>\tprofile HMM name list\n'
help += '-d <hmm file>\tprofile HMM dataset\n'
help += '\nOptional parameters:\n'
help += '-o <string>\toutput directory name (default: hmm_selected)'

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
      print("Profile HMM dataset (-d) not exist!")
      valid=False
    else:
      param["d"]=os.path.realpath(args.d)
  
  if valid==True:
    if not args.o==None:
      if os.path.isdir(args.o):
        print("Output directory (-o) {} exists!".format(args.o))
        out=rename(1,args.o,'dir')
        os.mkdir(out)
        print("Creating output directory (-o) {}...".format(out))
        param["o"]=out
      else:
       try:
         os.mkdir(args.o)
         print("Creating output directory (-o) {}...".format(args.o))
         param["o"]=args.o
       except:
         print("Output directory (-o) not valid\n")
         valid=False
    else:
     out=rename(1,'hmm_selected','dir')
     os.mkdir(out)
     print("Creating output directory (-o) {}...".format(out))
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
      log=open(os.path.join(param["o"], 'file.log'),'w')
      log.write('hmm_fetch v{}\n'.format(version))
      log.write('\nWorking directory:\n{}\n'.format(call))
      log.write('\nCommand line:\n{}\n'.format(' '.join(sys.argv)))
      log.write('\nParameters:\n{}\n'.format(str(param)))
      log.write('\nDataset analysis:')
    except:
      print('Log file was not created!')
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
          execution=datetime.now() - start_time
          print("\nExecution time: {}".format(execution))
          log.write("\nExecution time: {}".format(execution))
          print("Number of selected files: {}".format(len(selected)))
          log.write("\nNumber of selected files: {}".format(len(selected)))
          if selected==[]:
            print("All selected HMMs are missing!")
            log.write("\nAll selected HMMs are missing!\n")
          else:
            with open(os.path.join(param['o'], 'selected.hmm'),'w') as selectedfile:
              selectedfile.write('\n'.join(hmms))
            if missing==[]:
              print("All selected HMMs were saved!")
              log.write("\nAll selected HMMs were saved!\n")
            else:
              print("Missing HMMs:\t{}\n".format(missing.join(',')))
              log.write("\nMissing HMMs:\t{}\n".format(missing.join(',')))
              print("Selected HMMs:\t{}\n".format(selected.join(',')))
              log.write("Selected HMMs:\t{}\n".format(selected.join(',')))
            print("Execution time per file: {}".format(execution/len(selected)))
            log.write("Execution time per file: {}".format(execution/len(selected)))
      log.close()
            