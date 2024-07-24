from utils.mysql_utils import MysqlPool


class FlowList(object):

    def __init__(self):
        self.mysql_pool = MysqlPool()

    async def get_flow_list(self):


    async def get_all_article(self):
        select_sql = """
        select 
            a.pb_id, 
            pb_title, 
            ag.pb_name as pb_group_name, 
            pb_view_num, 
            pb_like_num, 
            DATE_FORMAT(a.Finsert_time, '%Y年%m月%d日 %H:%i:%s') AS Finsert_time, 
            DATE_FORMAT(a.Fmodify_time, '%Y年%m月%d日 %H:%i:%s') as Fmodify_time
        from 
            personal_blog_article a 
            join personal_blog_article_group ag on a.pb_group_id=ag.pb_id
        where 
            pb_permissions = 1 
        order by 
            pb_view_num desc, 
            pb_like_num desc 
        limit 100
        """
        results = await self.mysql_pool.select_mysql_all(select_sql)
        return results


