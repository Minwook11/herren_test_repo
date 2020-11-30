# 헤렌 코딩 테스트

# API Document
* [Herren test project API](https://documenter.getpostman.com/view/12271332/TVmJiegx)

# API List
#### Base API Address(AWS EC2) - http://52.78.152.195:8001
* 메일링 리스트 등록 API - POST
  * /mail/subscribe
  * Body = {"name" : "_NAME_", "email : "_EMAIL_"}
  
* 메일링 리스트에서 삭제 API - DELETE
  * /mail/unsubscribe
  * Body = {"email" : "_EMAIL_"}
  
* 메일 쓰기 API - GET
  * /mail/send
  * 기본적으로는 리스트에 등록된 모든 주소로 메일 송신
  * 쿼리스트링을 사용해서 target에 이메일을 넣으면 입력한 이메일로 송신
  
* 받은 메일 목록 API - GET
  * /mail/list?email="_EMAIL_"
  * 쿼리스트링을 사용해서 email에 입력한 메일 주소로 온 메일 목록 확인
