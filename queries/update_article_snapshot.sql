-- :name update_article_snapshot :insert
insert into ArticleSnapshot (article_id, raw_body)
values (:article_id, :raw_body)
