#!/usr/bin/env bash

# 이 프로젝트에 있는 모든 cronjob을 등록시켜주는 셸 스크립트
# timezone 설정하는 방법
# local설정을 원하는 timezone으로 맞춤(이상태에서는 cron에 적용되지 않음)
# sudo dpkg-reconfigure tzdata
# sudo service cron restart
# 정상 작동

setting_module="workout.settings"

# 인자는 settings의 위치임
if [ $# -eq 1 ]; then
    echo "django_setting_module set [$1]"
        setting_module=$1
fi

project_path=$( cd -P "$(dirname ${BASH_SOURCE[0]})/workout"&& pwd)
crons=$(find $project_path/.. -type d -name "cron" )
cron_env_tmp=$project_path"/cron_env_tmp"

#make cron_env_tmp(for crontab setting)
echo "################# ENVIRON #################" > $cron_env_tmp
echo "" >> $cron_env_tmp
echo "PYTHONPATH="$(printenv PYTHONPATH)":$project_path" >> $cron_env_tmp #현재 python path에 루트 디렉토리 추가
echo "DJANGO_SETTINGS_MODULE="$setting_module >> $cron_env_tmp #장고의 셋팅 파일 설정
printenv | grep SSULITE >> $cron_env_tmp
echo "SHELL=/bin/bash" >> $cron_env_tmp
echo "HOME=$(eval echo ~${SUDO_USER})" >> $cron_env_tmp
echo "DJANGO_HOME=$project_path" >> $cron_env_tmp
echo "" >> $cron_env_tmp
echo "################## CRONS ##################" >> $cron_env_tmp
echo "" >> $cron_env_tmp

setting_files="$cron_env_tmp "
echo "################ file list ################"
echo ""
for i in $crons
do
    find $i -type f -name "*.cnf"
    setting_files+=$(find $i -type f -name "*.cnf")
    setting_files+=" "
done
echo ""
echo "############## crontab register #############"
echo ""
cat $setting_files | crontab
rm $cron_env_tmp

crontab -l

