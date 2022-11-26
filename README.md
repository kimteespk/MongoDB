# Music Festival Trends from Spotify (Using Spotipy and MongoDB)
Application สำหรับดูเทรน และความแตกต่างระหว่างงาน Music Festival ต่างๆ โดยการใช้งานจะมีขั้นตอน

![image](https://user-images.githubusercontent.com/84601005/203669306-5f0234a2-fdd7-4810-983a-25a83b68b28c.png)

- การใช้งาน
  -  1 เพิ่ม Music Festival
  -  2 เพิ่ม ศิลปินที่แสดงในงานนั้นๆ (โดยการเพิ่ม Artist URI ของ Spotify เข้าไป)
  -  3 จากนั้นโปรแกรมจะดึง Top songs ของศิลปินนั้นๆ มาแสดงช่องขวามืออัตโนมัติ รวมถึงดึงข้อมูล Audio_Features, Popularites ของศิลปินจาก Spotify
  -  4 เลือกรายชื่อ Music Festival ที่ต้องการจะเปรียบเทียบ (select multiple) ในหน้าต่างด้านล่าง ละกด Plot โปรแกรมจะแสดงผล ค่าเฉลี่ยต่างๆ ของแต่ละ Festivals 
Fetching spotify audio features for each music festival and collect in MongoDB

# Notes

- Code จะแบ่งเป็น 3 ส่วน
ได้แก่ 
  - 1 Class FetchSpoty ที่จะใช้เชื่อมต่อและดึงข้อมูลจาก Spotify ซึ่งจะคัดเหลือข้อมูลที่ต้องการ และ return ออกมาในรูปแบบที่จะใช้เป็น Document ในแต่ละ Collection สำหรับ MongoDB

  - 2 Class MongoConnect ซึ่งทำหน้าเกี่ยวกับการเชื่อมต่อ MongoDB ละมีแต่ละ Function สำหรับทำการ CRUD ในแต่ละส่วนที่มี Method ในการจะเข้าไปถึงจุดที่ ข้อมูลที่อยู่ในส่วนต่างๆของ Document 

  - 3 ส่วน GUI และ Button/bind Functions ที่จะเป็นตัวเรียกใช้งาน Function ต่างๆที่เกี่ยวข้อง (Add, Delete, Plot และการ Update ที่ซ่อนอยู่ (ซึ่งจะเป็นการ Update array ที่เก็บข้อมูลศิลปิน ผ่านปุ่ม Add)) 

- ทุกขั้นตอนที่ใช้งานปุ่มใน GUI จะเชื่อมต่อกับ MongoDB ทั้งหมด
- การแสดงผลข้อมูลใน GUI จะมาจากการ Read ทั้งหมด
 
 # ลอง Plot ดู Features ของแต่ละเพลง ผ่านการ Double Click ที่เพลงที่ต้องการ
 ![image](https://user-images.githubusercontent.com/84601005/204041288-e9024818-2147-4909-a4fa-2d3973f11ee5.png)

 
 # Plot ดู Audio Features เฉลี่ยของ Music Festivals เพื่อเปรียบเทียบ
 ![image](https://user-images.githubusercontent.com/84601005/204041017-2bfb2d15-aee5-479f-b5ce-3a47da975211.png)

 # MongoDB
 - ส่วนของ Festival จะเก็บไว้ใน Collection ชื่อ Festival และจะมี Array ที่เก็บรายชื่อศิลปินทั้งหมดที่เล่นในงาน และ reference keys เพื่อเข้าถึง collection ที่เก็บ ข้อมูลของศิลปิน
 
 
 ![image](https://user-images.githubusercontent.com/84601005/204041564-50fb7195-bc8d-4c48-b2bb-165597400d92.png)

- ส่วนของ Artist จะอีก Collection หนึ่ง ซึ่งจะเก็บในรูปของ 1 ศิลปิน 1 Document, และใน Document จะมี array ที่เก็บ รายชื่อเพลง 10อันดับ ของศิลปิน และแต่ละเพลงก็จะเก็บ Audio Features ของเพลงนั้นๆ ไว้

![image](https://user-images.githubusercontent.com/84601005/204041606-2afa7094-2cc7-4fef-8d3b-a901cba85910.png)

# จุดบกพร่อง
- ข้อมูลที่เก็บใน MongoDB มีลักษณะเป็น Nested หลายชั้นมากเกินไป และทำให้ Aggregate ได้ยาก

