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
- db : MariaDB
- protocol : HTTP/HTTPS
- language : python django, django-rest-framework
- ssl : Let’s encrypt

# User API
회원관리 API(회원가입, 로그인, 회원정보조회 등)
## 로그인 (토큰흭득)
- URI : olloc.kr3.kr:8000/auth/
- METHOD : POST
- request

    | key | explanation | type |
    |--- |--- |--- |
    | username | user id | string |
    | password | password | string |

- response code
    - Header :
        Content-Type : application/json
    - ERROR RESPONSE
    
        |    key   | explanation |   type  |
        | -------- | ----------- |-------- |
        |error_code| 오류 코드     | integer | 
        |error_msg | 오류 내용  | string  |
        
        - error_code (오류 별 반환 내용 및 상태)
        
            | HTTP STATE | error_code | explanation |
            |----------- | ---------- | ----------- |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 401 |1| 토큰 만료 | 아이디에 특수문자 존재 등|
            | 401 |2| 토큰이 존재하지 않음|
    
    - SUCCESS RESPONSE
    
        | key | explanation | type |
        |--- |--- |--- |
        | token | 발급 토큰(클라이언트에서 저장하세요!) | string |
        | created | 토큰 발급 일 시 | string |

## 회원가입
- URI : olloc.kr3.kr:8000/user/
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
    - ERROR RESPONSE
    
        |    key   | explanation |   type  |
        | -------- | ----------- |-------- |
        |error_code| 오류 코드     | integer | 
        |error_msg | 오류 내용  | string  |
        
        - error_code (오류 별 반환 내용 및 상태)
        
            | HTTP STATE | error_code | explanation |
            |----------- | ---------- | ----------- |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 400 |1|아이디 유효성 오류 | 아이디에 특수문자 존재 등|
            | 400 |2|해당 회원이 데이터베이스 내 존재|
    
    - SUCCESS RESPONSE
        
        | key | explanation | type | remarks |
        | --- |------------ |----- | ------- |


## 회원정보 조회
- URI : olloc.kr3.kr:5000/v0.0/user/
- METHOD : GET
- request
    - Header : 
        - Content-Type : application/json

- RESPONSE
    - Header : 
        - Content-Type : application/json
        
    - ERROR RESPONSE
    
        |    key   | explanation |   type  |
        | -------- | ----------- |-------- |
        |error_code| 오류 코드     | integer | 
        |error_msg | 오류 내용     | string  |
    
        - error_code (오류 별 반환 내용 및 상태)
        
            | HTTP STATE | error_code | explanation |
            |----------- | ---------- | ----------- |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | ??? |1|아이디 유효성 오류 | 아이디에 특수문자 존재 등|
    
    - SUCCESS RESPONSE
    
        | key | explanation | type | remarks |
        | --- |------------ |----- | ------- |
        |name| 회원 이름 | string |
        |mail| 회원 이메일 | string |
        |name| 전화번호 | string | private : 비공개 |
        |pimg| 회원 프로필 사진 | string | 사진 URL |


# Post API

## 글 조회


## 글쓰기
- URI : olloc.kr3.kr:8000/post/
- METHOD : POST

- REQUEST :
    - Header : 
        - Content-Type : application/json
        - Authorization : 발급 된 토큰
    - Body : (json)

        | key | explanation | type |
        |--- |--- |--- |
        |description| 게시물 내용 | string |
        |contents| 사진 및 지도 | string |

    - ex)
    
- RESPONSE
    - Header : 
        - Content-Type : application/json
    - ERROR RESPONSE
    
        |    key   | explanation |   type  |
        | -------- | ----------- |-------- |
        |error_code| 오류 코드     | integer | 
        |error_msg | 오류 내용  | string  |
        
        - error_code (오류 별 반환 내용 및 상태)
        
            | HTTP STATE | error_code | explanation |
            |----------- | ---------- | ----------- |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 400 |1|아이디 유효성 오류 | 아이디에 특수문자 존재 등|
            | 400 |2|해당 회원이 데이터베이스 내 존재|
    
    - SUCCESS RESPONSE
        
        | key | explanation | type | remarks |
        | --- |------------ |----- | ------- |


## 댓글쓰기
## 좋아요


화평동 냉면 먹으러 가