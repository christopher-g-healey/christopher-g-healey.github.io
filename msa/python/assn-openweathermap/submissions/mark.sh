# -----
echo 'Tran David'
cd 'Tran David__dtran4ATncsu.edu__237084_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
echo 'Vogelsang Brett'
cd 'Vogelsang Brett__bavogelsATncsu.edu__237083_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
echo 'Willett Jason'
cd 'Willett Jason__jpwilletATncsu.edu__236998_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
echo 'Wilson Landon'
cd 'Wilson Landon__llwilso3ATncsu.edu__237033_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
echo 'Woelfel Nathan'
cd 'Woelfel Nathan__ncwoelfeATncsu.edu__237044_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
echo 'Wolschlag Andrew'
cd 'Wolschlag Andrew__apwolschATncsu.edu__237047_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
echo 'Zarrouk Nour'
cd 'Zarrouk Nour__nezarrouATncsu.edu__237010_assignsubmission_file_' > /dev/null
n=`ls -l ./*.py 2> /dev/null | wc -l`
if [[ $n -eq 0 ]]
then
  echo 'No .py file?'
elif [[ $n -eq 1 ]]
then
  rm -f *.csv*
  python3 *.py > /dev/null
  n=`ls -lR ./*.csv | wc -l`
  if [[ $n -eq 0 ]]
  then
    echo 'No CSV file created?'
  elif [[ $n -gt 1 ]]
  then
    echo 'More than one CSV file created?'
  else
    mv *.csv temp.csv
    echo '-----'
    n1=`diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv | wc -l`
    echo w/o USA: $n1
    if [[ $n1 -gt 0 ]]
    then
      diff -y -i -Z -b -W210 --suppress-common-lines ../weather_01.out temp.csv
    fi
  fi
else
  echo 'More than one .py file'
fi
cd ..
read -p 'Continue...'
# -----
