Verify if aaa config is there
"show running-config aaa"

if "no aaa new-model" found in output then add aaa config
else do not add aaa config

Verify if access-list 12 is already created
"show running-config | section access-list 12"

if matches then do not configure access-list

verify if access-lists permited in line vty

"show running-config | section line vty"

check if access-list 12 permitted or not,
if yes then just add "transport inpurt ssh"
else add both

