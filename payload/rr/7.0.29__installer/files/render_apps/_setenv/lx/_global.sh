#global environment for all render applications

echo we are logged in as:
id

#set USER and USERNAME if not set
if ( ! $?USERNAME ) then
  echo USERNAME is not set
  if ( ! $?USER ) then
    echo USER is not set
    setenv USER "`id -nu`"
    setenv USERNAME "$USER"
  else
    setenv USERNAME "$USER"
  endif
else
  if ( ! $?USER ) then
    echo USER is not set
    setenv USER "$USERNAME"
  endif
endif
echo USERNAME is set to $USERNAME
echo USER is set to $USER


#set home if it is not set right
if ( ! $?HOME ) then
  echo home is not set
  setenv HOME ~$USER
else
  echo home was set to $HOME
  setenv HOME ~$USER
endif
echo HOME is set to "$HOME"


#do not forget the empy line at the end:
