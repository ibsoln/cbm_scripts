import os

class utils:

  def getOutputFile( argName, argPath='_adoc_input', argOverwriteFile=false, argOverwritePath=false):
    msg=''
    result=False
    if(len(argName)>0):
      if(len(argPath)>0):
        if not(os.path.exists(argPath)):
          os.mkdir(argPath)
        thisFile=argPath+'/'+argName
        if(os.path.exists(thisFile)):
          msg='Path Already Exists'
        else:
          result = argPath + '/' + argName
      else:
        msg = 'No path provided'
    else:
      msg='File already exists'
    if(len(msg)>0): print(msg)
    return result
  # ENDDEF getOutPutFile

  def getOutputPath( argName, argPath='_adoc_input'):
    msg=''
    result=False
    if(len(argName)>0):
      if(len(argPath)>0):
        if not(os.path.exists(argPath)):
          os.mkdir(argPath)
        thisFile=argPath+'/'+argName
        if(os.path.exists(thisFile)):
          msg='Path Already Exists'
        else:
          result = argPath
      else:
        msg = 'No path provided'
    else:
      msg='File already exists'
    if(len(msg)>0): print(msg)
    return result
  # ENDDEF getOutPutFile
