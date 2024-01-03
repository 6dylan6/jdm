# jdm
线报监控专用，纯收集，无审查

ql repo https://github.com/6dylan6/jdm.git "jd_" "" "^jd[^_]|USER|function|sendNotify|magic|h5sts"

##一些变量（没写的看脚本内注释）

1、自定义sign

```
export JD_SIGN_KRAPI
```

2、使用代理池

```
export DP_POOL='http://192.168.1.200:8080'（代理池ip）

export PERMIT_JS='luck'（允许走代理的关键字）
```

代理api 

```
export DY_PROXY='api_url'（仅jd_wx_luckdraw支持）
```

3、自动填地址（报错就是变量不对，或者删除变量）

无线类（包含lzkj_loreal抽奖脚本）
```
export WX_ADDRESS="" # 变量格式：收件人@手机号@省份@城市@区县@详细地址@6位行政区划代码@邮编，需按照顺序依次填写，多个用管道符分开（6位行政区划代码自己查地图，也可用身份证号前六位）

export WX_ADDRESS_BLOCK="" # 多个关键词用@分开  黑名单

例子：export WX_ADDRESS="Z先生@13888888888@@江苏省@南通市@崇川区@开发区万科翡翠公园@320602@226001|K先生@13888888888@@江苏省@南通市@崇川区@开发区万科翡翠公园@320602@226001"
```

Jinggen(京耕)类
```
export jd_jinggeng_address="" # 变量格式：收件人@手机号@省份@城市@区县@详细地址，需按照顺序依次填写，多个用管道符分开

例子：export jd_jinggeng_address="Z先生@13888888888@江苏省@南通市@崇川区@开发区万科翡翠公园|K先生@13888888888@江苏省@南通市@崇川区@开发区万科翡翠公园"
```
