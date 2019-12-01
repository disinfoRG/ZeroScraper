"""add site airtable

Revision ID: da6f10c8ebf4
Revises: 95de751e529c
Create Date: 2019-11-29 07:48:18.074193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "da6f10c8ebf4"
down_revision = "da6f10c8ebf4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "Site", sa.Column("airtable_id", sa.String(256), nullable=True, unique=True)
    )
    try:
        upgrade_data()
        op.alter_column(
            "Site", "airtable_id", nullable=False, existing_type=sa.String(256)
        )
    except Exception as e:
        op.drop_column("Site", "airtable_id")
        raise e


def downgrade():
    op.drop_column("Site", "airtable_id")


sites = sa.sql.table(
    "Site",
    sa.Column("site_id", sa.Integer),
    sa.Column("url", sa.String(1024)),
    sa.Column("airtable_id", sa.String(256)),
)


def upgrade_data():
    for site_id, url in [
        (111, "https://www.youtube.com/channel/UCLZBXiS9ZrIXgKBs_SMfGBQ"),
        (58, "https://www.facebook.com/blesseverydayaroundyou/"),
    ]:
        op.execute(
            sites.delete().where(sites.c.site_id == site_id and sites.c.url == url)
        )

    for url, airtable_id in airtable_id_map.items():
        op.execute(
            sites.update()
            .where(sites.c.url == url)
            .values({"airtable_id": airtable_id})
        )


airtable_id_map = {
    ## XXX duplicated
    # "https://www.youtube.com/channel/UCLZBXiS9ZrIXgKBs_SMfGBQ":"rec8rzS7SqKqnQuio",
    "https://www.youtube.com/channel/UCmgDmqjxbkqIXu4rNbrKodA": "rectV3bxAU2YrpWQW",
    "https://www.youtube.com/channel/UCLZBXiS9ZrIXgKBs_SMfGBQ": "rec6OsbxedCXaW1j1",
    "https://www.youtube.com/channel/UCpu3bemTQwAU8PqM4kJdoEQ": "recYUDT5JflPA2OoF",
    "https://www.youtube.com/channel/UCN2e8dLY9KnH-B15LyBM7Fg": "recQWxWEaVUWUcWYX",
    "https://www.ptt.cc/bbs/HatePolitics/index.html": "recsh7wPi68vLDNWk",
    "https://www.ptt.cc/bbs/Gossiping/index.html": "recLVrfhLyQDCzDA8",
    "https://taronews.tw/": "recJFqGr5a1xfaf8o",
    "https://www.cna.com.tw/": "recQUiciCUROnBe4A",
    "http://news.ltn.com.tw/": "recMqu8b2B0fjCWIF",
    "https://udn.com/": "reci0cxTv83iSeHl8",
    "https://tw.appledaily.com/new/realtime": "recgBO5TsaGP8MLbg",
    "https://tw.appledaily.com/": "recW0Y3DQ3DaeRQ7Y",
    "https://www.ettoday.net/": "recJ9pSXGsxE4kmn9",
    "https://news.ebc.net.tw/": "recBW5P0o0fKX2T1L",
    "https://www.chinatimes.com/": "recslfJAoVKDbdh24",
    "https://www.eatnews.net/": "rec3Wrnrb3GTcDivT",
    "https://www.taiwanmazu.org/": "recB4NpLrTvUwWovp",
    "http://tailian.taiwan.cn/": "recG8g1JoHti4T8fO",
    "https://www.toutiao.com/": "recirH5ayaKXA633m",
    "http://www.itaiwannews.cn/": "reczA8cBEGIcvwo1B",
    "http://nooho.net": "recXoBEAH8TRdhZYj",
    "http://taiwan-madnews.com": "recXa7wpjdcrWT8X7",
    "http://taiwan-politicalnews.com": "recPnWuwH01QTAZPX",
    "http://hssszn.com": "recBpcl1dLZQpY2Q5",
    "http://fafa01.com": "recGN46B3LnnA8LbF",
    "http://qiqi.today": "recRl8ORrU0IKWkBZ",
    "http://defense.rocks": "recgFCKXWH8hBt6Rw",
    "http://cnba.live": "rec3HARifvZvpwmzE",
    "http://i77.today": "recSV8S0hvZY3ZTuA",
    "http://77s.today": "recgTV83ZY5NWWnGT",
    "http://www.qiqi.world/": "reca6qh8fo3mCqfCh",
    "http://www.mission-tw.com/mission": "recJjdr5Jb4fGe9Os",
    "http://www.taiwan.cn/": "recuC7NzKlui3dcd6",
    "https://www.facebook.com/eatnews/": "recQshOYa9lZin1AU",
    "https://www.facebook.com/search/top/?q=%E6%96%87%E5%B1%B1%E4%BC%AF&epa=SEARCH_BOX": "rec7xrqokEMg3s5L9",
    "https://www.facebook.com/znk168/": "recIjToauNtBJdyQu",
    "https://www.facebook.com/almondbrother/": "receHukPdyaKCtBMj",
    "https://www.facebook.com/Colorlessrise/": "recMSPrWl8AuExQMk",
    "https://www.facebook.com/pg/KSMissLin/groups/?referrer=pages_groups_card_cta&ref=page_internal": "rech9IRKLxxB0kx2w",
    "https://www.facebook.com/%E5%BC%B7%E5%BC%B7%E6%BB%BE%E5%A4%A7%E5%93%A5-%E9%98%BF%E8%AA%8C-1088027454701943/?__tn__=%2Cd%2CP-R&eid=ARBiDxJohZf5_icvMw2BXVNG2nHG4VR9b_ArA_Tc6PfA98MtdnGw1xVKWvIdE-X1wfSteOnhr6PxVDUX": "recx88UIQkLjJ10wU",
    "https://www.facebook.com/twherohan/": "recAY2H12zcSbCfhv",
    "https://www.facebook.com/%E8%A8%B1%E6%B7%91%E8%8F%AF-130771133668155/": "recvnH2Lot8ypWNrl",
    "https://www.facebook.com/hsiweiC/": "recVBlckyMtFmlh82",
    "https://www.facebook.com/groups/260112827997606/": "recIttcUl3HPUoqzj",
    "https://www.facebook.com/groups/391568921608431/": "recpKtnBclXwY4aqG",
    "https://www.facebook.com/groups/2072874742809044/": "recDffdw3nHCyVE3j",
    "https://www.facebook.com/groups/488305761638330/": "recm3eGGXPkOtfFLr",
    "https://www.facebook.com/groups/389408621877306/": "recdvH8v3SJX5TpRZ",
    "https://www.facebook.com/groups/768267203515635/": "recvKtQ84sirCdMzD",
    "https://www.facebook.com/straitstoday/": "recLmQSJ5BUyrpKE6",
    "https://www.facebook.com/youth86/": "recH6lOgxmwbsfu6N",
    "https://www.facebook.com/groups/1148919035153224/": "recw8GIqZ6a4HXzR4",
    "https://www.facebook.com/knowledge.practice.studio/": "rec7YTWk5wIUlQ25Z",
    "https://www.facebook.com/Templelivenetwork/": "recwAHI4ZH36ZOeeb",
    "https://www.facebook.com/%E4%B8%80%E8%B5%B7%E8%BF%BD%E5%8A%87%E5%90%A7-2407159445968433/": "recBYOI6sd8UPLnsm",
    "https://www.facebook.com/KMTTCC/": "reciCaICxxil0pnSj",
    "https://www.facebook.com/Quotations.life168/": "recGSreihqP7XX1C0",
    "https://www.facebook.com/ZhongHuaYRM/": "recfLM0dY6CKhVNuR",
    "https://www.facebook.com/happyworld88": "recMx7tumAkDqZulR",
    "https://www.facebook.com/traveltheworld168/": "recSdwgOnLSFlZajU",
    "https://www.facebook.com/yifanfengshun888/": "recQTMyEWf2xsCelK",
    "https://www.facebook.com/world.tw/": "rec5cEt7NvB3TcI79",
    "https://www.facebook.com/HaterIsHere/": "recTMSPJmmQXBfcDO",
    "https://www.facebook.com/jesusSavesF13/": "rechrvzObklDq6Xcj",
    "https://www.facebook.com/TaiwanNeutra/": "recANFv93ormFlTiT",
    "https://www.facebook.com/%E9%9F%93%E5%AE%B6%E8%BB%8D%E9%90%B5%E7%B2%89%E8%81%AF%E7%9B%9F-837868789721803/": "recc9xwpmhaoLMgzx",
    "https://www.facebook.com/%E7%B5%B1%E4%B8%80%E4%B8%AD%E5%9C%8B%E4%B8%AD%E5%9C%8B%E7%B5%B1%E4%B8%80-%E7%BB%9F%E4%B8%80%E4%B8%AD%E5%9B%BD%E4%B8%AD%E5%9B%BD%E7%BB%9F%E4%B8%80-1403317033298680/": "recmv1QvbaruPxERN",
    "https://www.facebook.com/%E5%8F%8D%E8%94%A1%E8%8B%B1%E6%96%87%E7%B2%89%E7%B5%B2%E5%9C%98-257062087822640/": "recLTcnCQdOyMgZX4",
    "https://www.facebook.com/CTTATTACK/": "recuhN7EituL81XfD",
    "https://www.facebook.com/Gyhappyboard/": "recUfUuenCqEXY13X",
    "https://www.facebook.com/%E8%A9%B1%E8%AA%AA%E9%82%A3%E4%BA%9B%E7%B7%A8%E9%80%A0%E7%9A%84%E4%BA%8B-304688810020434/": "rec4z05fcic3vlQyq",
    ## XXX duplicated
    # "https://www.facebook.com/blesseverydayaroundyou/":"recUUs0ITu6PrpVIo",
    "https://www.facebook.com/%E8%94%A1%E8%8B%B1%E6%96%87%E4%B8%8B%E5%8F%B0%E7%BD%AA%E7%8B%80%E9%9B%86%E7%B5%90%E7%B8%BD%E9%83%A8-121570255108696/": "reclAN9s2yWASp9A8",
    "https://www.facebook.com/CapricornStory4U/": "recLduxn9D5XD2w3p",
    "https://www.facebook.com/blesseverydayaroundyou/": "recVQ6iGSGFFAuK3I",
    "https://www.facebook.com/inability.dpp/": "recojKVhcsmrUQVrV",
    "https://www.facebook.com/%E8%97%8D%E8%89%B2%E6%AD%A3%E7%BE%A9%E5%8A%9B%E9%87%8F-1100522356652838/": "recm0Qil3pdQRPJq3",
    "https://www.facebook.com/LIKEHISTORYWORLD/": "recaSQDs9KIuUZL3g",
    "https://www.facebook.com/GCAironbloodarmy/": "recxjVgJQ4QA7vnP2",
    "https://www.facebook.com/globalchinesenewsunion/": "recS0IahdjcUZ2uV5",
    "https://www.facebook.com/GlobalChineselove/": "recXvfkeYIWRS1yDG",
    "https://www.facebook.com/cbcarmy/": "rec0GLO9KrkL26Hl9",
    "https://www.facebook.com/Islandofghost/": "recaxv1mbJzhBUmvh",
    "https://www.facebook.com/GhostIslandNews/": "recnfmS6KQq8ADPdq",
    "https://www.facebook.com/lovebakinglovehealthy/": "recqDcHtzstSEYuEN",
    "https://www.facebook.com/getoutdpp/": "recGhjG3J67YawoV3",
    "https://www.facebook.com/%E7%BD%B7%E5%85%8D%E6%B0%91%E9%80%B2%E9%BB%A8-2129370967290567/": "rec3rJ5tNg2otD5qz",
    "https://www.facebook.com/johncelayo/": "rec8n4wKSsbOAyq1J",
    "https://www.facebook.com/grumbledpp/": "rec64LvmyaPlP4kBP",
    "https://www.facebook.com/%E6%96%87%E9%9D%92%E5%B7%A5%E4%BD%9C%E6%9C%83-510052339062419/": "rec8Z1YuT8hWKYbG2",
    "https://www.facebook.com/%E9%9D%A0%E5%8C%97%E6%B0%91%E9%80%B2%E9%BB%A8-454656575008713/": "recwLUUVEocoCeT8g",
    "https://www.facebook.com/bigchinalove/": "recPUgrixj8HPlVUp",
    "https://www.facebook.com/shengser/": "rec63fhQeP0MU3357",
    "https://www.facebook.com/%E8%A8%8E%E5%8E%AD%E6%B0%91%E9%80%B2%E9%BB%A8-504021696772145/": "rec7l2nBPLFj4sOmr",
    "https://www.facebook.com/%E9%9D%A0%E5%8C%97%E6%99%82%E4%BA%8B-165534787282102/": "recGCFPh0DWZ6MG4i",
    "https://www.facebook.com/taiwan1314520/": "rec9BS2RnG7Bi773d",
    "https://www.facebook.com/fuqidao168/": "recVbbS2hFI2S39z7",
    "https://www.facebook.com/GlobalChineseAlliance/": "recEvRHB5bqjxS6ES",
    "https://www.facebook.com/%E5%A4%A9%E5%8D%97%E5%9C%B0%E5%8C%97-1063653903655415/": "recdWAeftdXBwOLIX",
    "https://www.facebook.com/kmtdppisshit/": "rec6s2d1TXlmUI2nG",
    "https://www.facebook.com/catssssssssssssss/": "recpu60Ei5EqoEXxn",
    "https://www.facebook.com/qiqi.news/": "recOpNLBJ4R2mmCqM",
    "https://www.facebook.com/dogcat101300/": "recXy5Rkxp0PhMpCs",
    "https://www.facebook.com/travelmoviemusic/": "recw9FN2e3jZFJwqX",
    "https://www.facebook.com/imangonews/": "recVrU412hfv2dChw",
    "https://www.facebook.com/%E4%BA%BA%E7%94%9F%E6%AD%A3%E8%83%BD%E9%87%8F-1349834938455966/": "reccVfkXwa6u8R4o3",
    "https://www.facebook.com/%E4%BA%BA%E7%94%9F%E7%AC%91%E8%91%97%E8%B5%B0-1958092751106755/": "recEnSF53PkWENrhs",
    "https://www.facebook.com/thumbsuplifenews/": "recqbh2I61V2JArRi",
    "https://www.facebook.com/hssszn/": "recODAxW73l6JpJJ7",
    "https://www.facebook.com/aroundtheworld01/": "recjrgKJKwH1ru67m",
    "https://www.facebook.com/%E5%8F%8D%E8%94%A1%E8%8B%B1%E6%96%87%E8%81%AF%E7%9B%9F%E5%85%A8%E5%9C%8B%E6%B0%91%E6%80%A8%E5%97%86%E8%94%A1%E7%B8%BD%E9%83%A8-1566024720346478/": "rectYderJ2wfojGfN",
    "https://www.facebook.com/%E9%9D%92%E5%A4%A9%E7%99%BD%E6%97%A5%E6%AD%A3%E7%BE%A9%E5%8A%9B%E9%87%8F-1006889099430655/": "recjnR3SPoTTEUT15",
    "https://www.guancha.cn/": "recE5pFRI2dRUdsBB",
    "https://news.163.com": "recqZh8SLNtPITFo9",
    "https://kknews.cc/": "recKJwOC1QvSQJgKB",
    "http://www.readthis.one/": "recxMOjlGZDoUbLWc",
    "https://www.coco01.today/": "recjILSLlLRmkgP5I",
    "https://www.ptt01.cc/": "recj4kR6ExZgXdzOk",
    "https://www.xuehua.us/": "recbEZkJV8k2Fg91E",
    "https://www.orgs.one/": "recJVUAsWSsbKz9N0",
    "http://www.how01.com/": "rec03ujV04yeDHeAu",
    "https://read01.com/zh-tw/": "recwO0vYEkxI4JbBl",
    "https://www.youtube.com/channel/UCgkHTZsCdH8P9z7lazTXN3g": "recnUmD0TFC1UPMPH",
    "https://www.youtube.com/channel/UCJHq28mKJowPCGQ0WDIDU9A": "recjh6Rzp8iCarxF3",
    "https://www.youtube.com/channel/UCMcDqLHgIuXWtWsqPEkqnWA": "recyUFTVMNsGGuCAV",
}
