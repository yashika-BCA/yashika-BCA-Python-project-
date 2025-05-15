create database SOCIAL_MEDIA_PLATFORM;
use SOCIAL_MEDIA_PLATFORM;


SELECT 
    *
FROM
    accounts;
SELECT 
    *
FROM
    profile;
SELECT 
    *
FROM
    users;
SELECT 
    *
FROM
    post;
SELECT 
    *
FROM
    story;
SELECT 
    *
FROM
    live;
set sql_safe_updates=0;
UPDATE users 
SET 
    official_account = 'Blue tick'
WHERE
    users_id = 2;
alter table users
change column Blue_tick  official_account varchar(25);

CREATE TABLE post (
    users_id INT,
    FOREIGN KEY (users_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    user_name VARCHAR(35),
    post_id INT NOT NULL PRIMARY KEY,
    post_type VARCHAR(25),
    post_path VARCHAR(100),
    dated DATE,
    likes INT,
    comments VARCHAR(25),
    audiance VARCHAR(25) CHECK (audiance = 'everyone'
        OR audiance = 'close_friends')
);


CREATE TABLE story (
    users_id INT,
    FOREIGN KEY (users_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    user_name VARCHAR(35),
    dated DATE,
    location VARCHAR(25) CHECK (location = 'yes' OR location = 'no'),
    music VARCHAR(25) CHECK (music = 'yes' OR music = 'no'),
    tag INT,
    views VARCHAR(100) CHECK (views = 'close friends'
        OR views = 'Everyone'
        OR views = 'Both'),
    likes INT
);  
                  
truncate story;
insert into post
values
(2,"druv",101,"Reel","landscape/video/slideshow.avi","2024-08-04",13,5,"everyone"),
(4,"gaurav99",107,"Image","outfit.pinterest.com","2024-08-01",29,2,"everyone"),
(7,"sham",111,"video","VV/count/video.mp4","2024-08-06",25,12,"everyone"),
(8,"goli",112,"Image","dot/image/picture.png","2024-08-10",23,15,"everyone"),
(9,"tappu00",113,"video","<vacation>src/youcut.avi","2024-08-15",26,7,"everyone"),
(12,"raghav",120,"Reel","duel/lite/visual.mp4","2024-08-05",19,4,"everyone"),
(13,"veer",123,"Image","pet.pinterest.com//","2024-08-09",3,0,"Close_friends"),
(14,"sonu",126,"video","emerge/moshion/vishual.mov","2024-08-01",7,1,"everyone"),
(15,"geeta_",129,"Reel","112xyz/youcut/images.mov","2024-08-16",0,0,"Close_friends");

insert into story
values
(2,"abhi","2024-07-30","yes","no",5,"everyone",30),
(4,"gaurav99","2024-08-05","yes","yes",1,"everyone",29),
(6,"radhika05","2024-08-11","yes","no",0,"close friends",5),
(7,"sham","2024-08-02","yes","yes",3,"everyone",28),
(8,"goli","2024-07-15","no","yes",1,"everyone",30),
(9,"tappu00","2024-08-17","no","yes",0,"everyone",29),
(11,"cute disha","2024-07-19","yes","no",2,"close friends",5),
(12,"raghav","2024-08-01","no","no",0,"everyone",30),
(13,"veer_","2024-08-04","yes","yes",6,"close friends",6),
(14,"sonu","2024-08-06","no","no",3,"everyone",15),
(15,"geeta_","2024-07-17","yes","yes",1,"close friends",2);

CREATE TABLE live (
    users_id INT,
    FOREIGN KEY (users_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    user_name VARCHAR(35),
    live_id INT NOT NULL PRIMARY KEY,
    dated DATE,
    started_at VARCHAR(50),
    duration VARCHAR(100),
    chat VARCHAR(25) CHECK (chat = 'on' OR chat = 'off'),
    views INT,
    likes INT
);  
drop table live;
truncate live;
insert into live
values
(3,"vishu",1001,"2024-8-15","09:30 am","1 hour","off",35,19),
(6,"radhika05",1011,"2024-7-30","11:45 am","1.5 hours","off",24,11),
(9,"tappu00",1014,"2024-8-22","05:00 pm","2.5 hours","on",50,35),
(11,"cute_disha",1022,"2024-8-16","09:00 pm","1 hour","off",15,10),
(12,"raghav",1025,"2024-7-28","01:30 pm","3 hours","on",55,32),
(13,"veer",1030,"2024-8-19","06:20 pm","2 hour","on",19,13);

use social_media_platform;
SELECT 
    *
FROM
    live;

CREATE TABLE message (
    users_id INT,
    FOREIGN KEY (users_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    user_name VARCHAR(35),
    chat_id INT,
    FOREIGN KEY (chat_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    chat_type VARCHAR(55) CHECK (chat_type = 'Group'
        OR chat_type = 'Individual'),
    last_seen VARCHAR(50),
    chat_status VARCHAR(25) CHECK (chat_status = 'Typing..'
        OR chat_status = 'Recording..'
        OR chat_status = '-'),
    shareed_content VARCHAR(25) CHECK (shareed_content = 'image'
        OR shareed_content = 'video'
        OR shareed_content = 'audio'
        OR shareed_content = 'docc.'
        OR shareed_content = 'text')
);

drop table message;
insert into message
values
(2,"abhi",8,"group","(Today)5 pm","-","text"),
(4,"Gaurav99",14,"individual","online","typing..","docc."),
(7,"sham",12,"individual","online","recording..","video"),
(8,"goli",2,"group","online","typing..","image"),
(12,"raghav",7,"individual","(today)10 am","-","text"),
(14,"sonu",4,"individual","(today)2 pm","-","image"),
(15,"geeta",2,"group","online","typing..","text");

SELECT 
    *
FROM
    message;

create table groups_(
group_id int not null primary key,
group_name varchar(25),
members int,
admin varchar(55), foreign key(admin) references profile(user_name)
);
drop table message;
insert into groups_
values
(191,"edu.query",11,"gaurav99"),
(181,"chopsy",9,"raghav"),
(171,"podcast",9,"tappu00");


SELECT 
    *
FROM
    groups_;

drop table groups_;
SELECT * FROM social_media_platform.profile;


alter table profile;

CREATE TABLE collab (
    users_id INT,
    FOREIGN KEY (users_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    user_name VARCHAR(35),
    collab_type varchar(40) check(collab_type="brand" or collab_type="profile"),
    posts_id int , foreign key(posts_id) references post(post_id) on update cascade,
    lives_id int , foreign key(lives_id) references live(live_id) on update cascade,
    purpose VARCHAR(35) CHECK (purpose = 'marketing' OR purpose = 'influencing'),
    charges int
);  
select*from colabe;


insert into collab
values
(2, 'abhi', 'brand', 101, NULL, 'marketing', 2500),
(7, 'sham', 'brand', 111, NULL, 'marketing', 5500),
(8, 'goli', 'profile', 112, NULL, 'influencing', 5800),
(9, 'tappu00', 'profile', 113, '1014', 'influencing', 5000),
(12, 'raghav', 'brand', 120, '1025', 'marketing', 5215);

CREATE TABLE INCOME(
    users_id INT,
    FOREIGN KEY (users_id)
        REFERENCES accounts (user_id)
        ON UPDATE CASCADE,
    user_name VARCHAR(35),
    Monthly_income int,
    collab int,
    profile varchar(25) check(profile="personal" or profile="profetional"),
    blue_tick varchar(25) check(blue_tick="yes" or blue_tick="no")
);  
desc income;
insert into income
values
(2,"abhi",6250,1,"profetional","yes"),
(4, 'gaurav99',7800,0,"profetional", 'no'),
(7, 'sham',9250, 1,"profetional", 'yes'),
(8, 'goli',9500, 1, 'profetional', 'yes'),
(9, 'tappu00',9810, 1, 'profetional', 'yes'),
(12, 'raghav', 6910,0, 'personal', 'no'),
(14, 'sonu', 4200, '0', 'personal', 'no');

use social_media_platform; 
select*from accounts; 
select*from users;#work #educatin #city #relationship
select*from profile;
select*from message; #active_now #recent #message_request #community
select*from groups_;
select*from post;
select*from story;
select*from live;
select*from collab;
select*from income;
select*from personal_information; #signup_date #city #relationship
select*from most_active_accounts;

alter table accounts add column signup_date varchar(25);
alter table users add column work varchar(25)  ;
alter table users add column education varchar(25);
alter table users add column city varchar(25);
alter table users modify column relationship varchar(30) check(relationship ="single" or relationship ="maried" or relationship ="in relation");
alter table message rename column user_name to active_now;
alter table message add column message_request int;
alter table message add column recent varchar(25);
alter table message drop column last_seen;
alter table message drop column recent;
alter table message drop column shareed_content;
set sql_safe_updates=0;
update message 
set chat_status="typing.."
where users_id=12;
alter table groups_ add column group_type varchar(25) check(group_type ="community" or group_type ="chanel" or group_type ="group");

update users 
set relationship="maried"
where users_id=15;

select*from users;

update message
set chat_id=3
where chat_id=7;

use social_media_platform;
# sign up date;
# relationship;
create view Most_active_accounts as select a.user_id,a.user_name, a.account_status , u.official_account , p.posts,p.followers,p.following,m.last_seen, o.likes as post_likes,s.likes as story_likes,l.duration as live_time,l.views as live_views,l.likes as live_likes,c.posts_id as collab_post_id,c.lives_id as collab_live_id,i.monthly_income
from
accounts a join users u on a.user_id = u.users_id join profile p on p.users_id = u.users_id join message m on m.users_id = p.users_id join post o on o.users_id = m.users_id join story s on s.users_id = o.users_id join  live l on l.users_id = s.users_id join collab c on c.users_id = l.users_id  join income i on i.users_id = c.users_id;

drop view personal_information;
select*from most_active_accounts;

create view personal_information as
select a.user_id,a.user_name,a.email_address,a.phone_number,a.birthday,a.signup_date,u.gender,u.city,u.relationship,p.blocked_accounts
from 
accounts a join users u on a.user_id=u.users_id join profile p on u.users_id=p.users_id;

select*from personal_information;

use social_media_platform;
# view 3 users feed view 4 popularity
# queries
#role user 
# script
# note