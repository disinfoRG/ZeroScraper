-- :name find_first_article :one
select * from Article
where url = :url
