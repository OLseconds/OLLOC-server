# OLLOC-server
해당 프로젝트는 위치기입에 강제성을 띄우는 SNS 제작 프로젝트이다.

해당 레파지토리는 백엔드 부분임 

프론트엔드 레파지토리 : https://github.com/O-Seonsik/OLLOC

# 해당 프로젝트 포스팅
- https://leejh.info/archives/232
- https://leejh.info/archives/270
- https://leejh.info/archives/276
- https://leejh.info/archives/284


# 작업환경
- server : azure 가상머신
- os : ubuntu 18.04 LTS
- db : mongodb
- protocol : HTTP/HTTPS
- language : python (+flask)
- ssl : Let’s encrypt

# User API
회원관리 API(회원가입, 로그인, 회원정보조회 등)
## 로그인
- URI : olloc.kr3.kr:5000/v0.0/user/session
- METHOD : POST
- request

| key | explanation | type |
|--- |--- |--- |
| username | user id | string |
| password | password | string |
|
- response code

## 회원가입
- URI : olloc.kr3.kr:5000/v0.0/user/join
- METHOD : POST
- REQUEST :
    - Header : 
        - Content-Type : application/json
    - Body : (json)

        | key | explanation | type |
        |--- |--- |--- |
        |username| 회원 아이디 | string |
        |password| 회원 패스워드 | string |
        |name| 회원 이름 | string |
        |mail| 회원 이메일 | string |
    - ex)
        - { "username": "test2", "password": "world", "name":"jonghwi", "mail":"ddd@kookmin.ac.kr"}
- RESPONSE
    - Header : 
        - Content-Type : application/json
    
    | key | explanation | type | remarks |
    | --- |------------ |----- | ------- |
    |error_code| 오류 코드  | integer | 0 : 파라미터 오류 , 1 : 아이디 유효성 오류 , 2 : 이미 해당 회원 존재
    |error_msg| 오류 상세내용 | string |
    |name| 회원 이름 | string |
    |mail| 회원 이메일 | string |

## 회원정보 조회
- URI : olloc.kr3.kr:5000/v0.0/user/user_profile
- METHOD : POST
- request

| key | explanation | type |
|--- |--- |--- |
|  | dd | dd |
- response code

# Location API
## 글쓰기
## 댓글쓰기
## 좋아요


화평동 냉면 먹으러 가