# OLLOC-server
해당 프로젝트는 위치기입에 강제성을 띄우는 SNS 제작 프로젝트이다.

해당 레파지토리는 백엔드 부분임 

Thanks to @zaeval

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
- URI : olloc.kr3.kr:8000/user/
- METHOD : GET
- request
    - Header : 
        - Authorization : 발급 된 토큰

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
            | 400 |-1| 토큰에러 auth 로그인 참고 |
    
    - SUCCESS RESPONSE
    
        | key | explanation | type | remarks |
        | --- |------------ |----- | ------- |
        |id| 회원 번 | integer |
        |username| 회원 아이디  | string |
        |email| 회원 이메일 | string |  |
        |is_superuser| 관리자 여부 | boolean |  |
        |is_active| 활성화 여부 | boolean |  |
        |follower|팔로워 수 | integer|
        |following|팔로잉 수 | integer|
        
{
"id": 1,
"username": "paperlee",
"name": "이종휘",
"email": "paperlee@kookmin.ac.kr",
"is_superuser": false,
"is_active": true
}

## 팔로잉
- URI : olloc.kr3.kr:8000/follow/
- METHOD : POST
- request
    - Header : 
        - Authorization : 발급 된 토큰
        - Content-Type : application/json
    - Body : (json)
    
        | key | explanation | type |
        |--- |--- |--- |
        |user_id|팔로잉 대상 user number| integer|
        
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
            | 400 |-1| 토큰에러 auth 로그인 참고 |
            | 400 | 0 | 파라미터 오류 |
            | 400 | 1 | 팔로잉 대상이 올바르지 않음 |
    
## 언팔로잉
- URI : olloc.kr3.kr:8000/follow/
- METHOD : DELETE
- request
    - Header : 
        - Authorization : 발급 된 토큰
        - Content-Type : application/json
    - QUERY PARAMETER : 
 
        | key | explanation | type |
        |--- |--- |--- |
        |user_id|팔로잉 대상 user number| integer|
        
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
            | 400 |-1| 토큰에러 auth 로그인 참고 |
            | 400 | 0 | 파라미터 오류 |
            | 400 | 1 | 언팔로잉 대상이 올바르지 않음 |
            | 400 | 2 | 언팔로잉 대상이 팔로잉 중이지 않음 |

# Post API

## 글 조회
- URI : olloc.kr3.kr:8000/posts/
- METHOD : GET

- REQUEST :
    - Header : 
        - Authorization : 발급 된 토큰
    - QUERY PARAMETERS  : 

        | key | explanation | type |
        |--- |--- |--- |
        |post_id| 게시물 번호 | string |
    
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
            | 400 |-1| 토큰에러 auth 로그인 참고 |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 400 |1|아이디 유효성 오류 | 아이디에 특수문자 존재 등|
            
    - SUCCESS RESPONSE
        
        |   key  | explanation | type | remarks |
        | ------ | ----------- |----- | ------- |
        |id | 게시물 번호   |integer |
        |owner | 게시물 소유자   | integer |
        |last_modified | 마지막 수정시간 | time |
        |description | 게시물 내 |string |
        |lx| 지도 x값 | array(string)|
        |ly| 지도 y값 | array(string)|
        |map_info|맵설명|array(string)|
        |img| 사진 | array(string)|
        
       

## 글쓰기
- URI : olloc.kr3.kr:8000/posts/
- METHOD : POST

- REQUEST :
    - Header : 
        - Content-Type : multipart/form-data
        - Authorization : 발급 된 토큰
    - Body : (Form)

        | key | explanation | type |
        |--- |--- |--- |
        |image| 이미지파일 from data | string |
        |lx| 지도 x 값 | string |
        |ly| 지도 y 값 | string |
        |map_info| 지도 상세내용| string|
        |content| 게시물내용 | string |
    
- RESPONSE
    - Header : 
        - Content-Type : application/json
    - ERROR RESPONSE
    
        |    key   | explanation |   type  |
        | -------- | ----------- |-------- |
        |error_code| 오류 코드     | integer | 
        |error_msg | 오류 내용  | string  |
        |error_file| 오류원인 파일| string |
        
        - error_code (오류 별 반환 내용 및 상태)
        
            | HTTP STATE | error_code | explanation |
            |----------- | ---------- | ----------- |
            | 400 |-1| 토큰에러 auth 로그인 참고 |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 400 |1|업로드 파일 형식 오류 image/XXX 이 아님 | 아이디에 특수문자 존재 등|
            

    
    - SUCCESS RESPONSE
        
        | key | explanation | type | remarks |
        | --- |------------ |----- | ------- |
## 글 삭제
- URI : olloc.kr3.kr:8000/posts/
- METHOD : DELETE

- REQUEST :
    - Header : 
        - Authorization : 발급 된 토큰
    - QUERY PARAMETERS  :

        | key | explanation | type |
        |--- |--- |--- |
        |post_id| 삭제할 게시물 번호 | integer |
    
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
            | 400 |-1| 토큰에러 auth 로그인 참고 |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 400 |1| 해당 게시물이 존재하지 않 |
            | 400 |2| 해당 게시물이 본인 소유가 아님 |


## 댓글쓰기
- URI : olloc.kr3.kr:8000/comment/
- METHOD : POST

- REQUEST :
    - Header : 
        - Content-Type : application/json
        - Authorization : 발급 된 토큰
    - Body :

        | key | explanation | type |
        |--- |--- |--- |
        |post_id| 대상 게시물 id | string |
        |description| 댓글 내용 | string |
    
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
            | 400 |-1| 토큰에러 auth 로그인 참고 |
            | 400 |0| 파라미터 오류, 상세 내용은 error_msg 참고 |
            | 400 |1| 해당 게시물이 존재하지 않음 | 
            

    
    - SUCCESS RESPONSE
        
        | key | explanation | type | remarks |
        | --- |------------ |----- | ------- |
## 좋아요

# 냉면 맛집면
- NAME : 숙이네 왕냉면
- URI : 37.4229729,126.648891
-------
- NAME : 육쌈냉면 송도점
- URI : 37.3970124,126.6399748
-------
- NAME : 별미칡냉면 부평 갈산동
- URI : 37.5111495,126.7032001
