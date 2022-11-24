# Music Festival Trends by Spotify (Using Spotipy and MongoDB)
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
 
 
TODO 
- แปะรูป GIF การทำงานของ GUI



- แปะรูป Database(Collection and Document) Design

