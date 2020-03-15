-- :name insert_stats :insert
insert into SiteStats (site_id, date, new_posts_count, revisit_posts_count)
values (:site_id, :date, :discover_count, :update_count)