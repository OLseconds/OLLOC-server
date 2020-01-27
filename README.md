# OLLOC-server
해당 프로젝트는 위치기입에 강제성을 띄우는 SNS 제작 프로젝트이다.

해당 레파지토리는 백엔드 부분임 

https://leejh.info/archives/232

- server : azure 가상머신
- os : ubuntu 18.04 LTS
- db : mongodb
- protocol : HTTP/HTTPS
- language : python (+flask)
- ssl : Let’s encrypt

#API

# User API
회원관리 API(회원가입, 로그인, 회원정보조회 등)
## 로그인
- URI : azure.kr3.kr/v0.0/user/login
- METHOD : POST
- request

| key | explanation | type |
|--- |--- |--- |
|  | dd | dd |
- response code
## 회원가입
- URI : azure.kr3.kr/v0.0/user/join
- METHOD : POST
- request

| key | explanation | type |
|--- |--- |--- |
|  | dd | dd |
- response code
## 회원정보 조회
- URI : azure.kr3.kr/v0.0/user/user_profile
- METHOD : POST
- request

| key | explanation | type |
|--- |--- |--- |
|  | dd | dd |
- response code

# Location API
## 글쓰기
## 댓글쓰기
## ~~(너가)~~좋아요


화평동 냉면 먹으러 가자