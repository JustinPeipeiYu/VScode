WMIC USERACCOUNT WHERE Name="administrator" SET PasswordExpires=True
net accounts /maxpwage: 30
net user "administrator"
net user user_name /passwordreq:yes
