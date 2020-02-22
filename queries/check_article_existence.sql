-- :name check_article_existence :one
SELECT EXISTS(SELECT article_id from Article WHERE url=:url) as exist;