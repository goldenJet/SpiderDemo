create database scrapy DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use scrapy;
-- drop TABLE if EXISTS douban_movie_top_250;
CREATE TABLE douban_movie_top_250 (
		id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    film_name VARCHAR(255) NOT NULL comment '电影名字',
    director_performer_name VARCHAR(255) comment '导演和主演名字',
		film_year VARCHAR(10) comment '电影上映年份',
		film_country VARCHAR(255) comment '电影国家',
		film_type VARCHAR(255) comment '电影类型',
		film_rating VARCHAR(10) comment '电影评分',
		film_reviews_num VARCHAR(10) comment '电影评论人数',
		film_quato VARCHAR(255) comment '电影经典语句',
		film_img_url VARCHAR(255) comment '电影图片URL'
) COMMENT="豆瓣电影排名TOP250"
