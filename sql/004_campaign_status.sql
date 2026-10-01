-- added oct 2026. run after 003
alter table campaign add column if not exists status text not null default 'active';   -- active | archived
