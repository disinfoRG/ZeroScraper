-- :name get_sites_to_crawl :many
select site_id, name, last_crawl_at from Site
where is_active=1 and type in ('official_media', 'content_farm', 'organization_website', 'news_website')
order by last_crawl_at asc
