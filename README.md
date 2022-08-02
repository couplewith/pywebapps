

#




# 문제 해결

## github push 해결
- SSL certificate problem

  * git push ...


```
[푸시 실패]
unable to access 'https://github.com/couplewith/pyweb3.git/': SSL certificate problem: self signed certificate in certificate chain
```

 - PS pyweb3> cmd
 - PS pyweb3> "C:\Program Files\Git\bin\git.exe" config http.sslVerify false
.git/config
 - PS pyweb3> cat .\.git\config

```
[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	symlinks = false
	ignorecase = true
[remote "origin"]
	url = https://github.com/couplewith/pyweb3.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[http]
	sslVerify = false

```