# -*- coding: UTF-8 -*-
from typing import List

from twitter import Status, Url, User

basic_tweet: Status = Status(
    **{
        "created_at": "Sun Dec 15 03:48:03 +0000 2019",
        "favorite_count": 1,
        "hashtags": [],
        "id": 1206058311864528896,
        "id_str": "1206058311864528896",
        "in_reply_to_screen_name": "FTBandFTR",
        "in_reply_to_status_id": 1206055345795346432,
        "in_reply_to_user_id": 842188154698399746,
        "lang": "en",
        "source": '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
        "text": "If someone wants off the list that\u2019s okay. I will remove them ASAP.",
        "urls": [],
        "user": User(
            **{
                "created_at": "Thu Mar 16 01:37:58 +0000 2017",
                "default_profile": True,
                "description": "If someone wants off the list that\u2019s okay. I will remove them ASAP. This account auto screen caps tweets that are quoted by select users I @_b_axe follow.",
                "favourites_count": 14,
                "followers_count": 32,
                "friends_count": 13,
                "id": 842188154698399746,
                "id_str": "842188154698399746",
                "location": "Austin, TX",
                "name": "For the blocked and For the record",
                "profile_background_color": "F5F8FA",
                "profile_image_url": "http://pbs.twimg.com/profile_images/1195922003615727617/hhgc1XSp_normal.jpg",
                "profile_image_url_https": "https://pbs.twimg.com/profile_images/1195922003615727617/hhgc1XSp_normal.jpg",
                "profile_link_color": "1DA1F2",
                "profile_sidebar_border_color": "C0DEED",
                "profile_sidebar_fill_color": "DDEEF6",
                "profile_text_color": "333333",
                "profile_use_background_image": True,
                "screen_name": "FTBandFTR",
                "statuses_count": 2573,
            }
        ),
        "user_mentions": [],
    }
)
quoted_tweet: Status = Status(
    **{
        "created_at": "Sat Jan 18 21:13:57 +0000 2020",
        "favorite_count": 1290,
        "hashtags": [],
        "id": 1218642707586977797,
        "id_str": "1218642707586977797",
        "lang": "en",
        "quoted_status": Status(
            **{
                "created_at": "Sat Jan 18 20:57:50 +0000 2020",
                "favorite_count": 4633,
                "hashtags": [],
                "id": 1218638650726146050,
                "id_str": "1218638650726146050",
                "lang": "en",
                "retweet_count": 723,
                "source": '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
                "text": "The \u201cbody language expert\u201d Joy-Ann Reid had on to say Bernie Sanders lied at the debate posted anti-Vaxxer content\u2026 https://t.co/2kzeCWezvw",
                "truncated": True,
                "urls": [
                    Url(
                        **{
                            "expanded_url": "https://twitter.com/i/web/status/1218638650726146050",
                            "url": "https://t.co/2kzeCWezvw",
                        }
                    )
                ],
                "user": User(
                    **{
                        "created_at": "Wed Jul 31 01:41:01 +0000 2013",
                        "default_profile": True,
                        "description": "Reporter @thenation. FOIA nerd. Signal: (202)510-1268. ken@thenation.com IG: https://t.co/dWf8CtPb8S",
                        "favourites_count": 78814,
                        "followers_count": 167460,
                        "friends_count": 4995,
                        "geo_enabled": True,
                        "id": 1634248890,
                        "id_str": "1634248890",
                        "listed_count": 1820,
                        "location": "DC",
                        "name": "Ken Klippenstein",
                        "profile_background_color": "C0DEED",
                        "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
                        "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
                        "profile_banner_url": "https://pbs.twimg.com/profile_banners/1634248890/1575269054",
                        "profile_image_url": "http://pbs.twimg.com/profile_images/1215764304085049345/P30L6eYQ_normal.jpg",
                        "profile_image_url_https": "https://pbs.twimg.com/profile_images/1215764304085049345/P30L6eYQ_normal.jpg",
                        "profile_link_color": "1DA1F2",
                        "profile_sidebar_border_color": "C0DEED",
                        "profile_sidebar_fill_color": "DDEEF6",
                        "profile_text_color": "333333",
                        "profile_use_background_image": True,
                        "screen_name": "kenklippenstein",
                        "statuses_count": 21451,
                        "url": "https://t.co/vmp3GTVJl5",
                        "verified": True,
                    }
                ),
                "user_mentions": [],
            }
        ),
        "quoted_status_id": 1218638650726146050,
        "quoted_status_id_str": "1218638650726146050",
        "retweet_count": 245,
        "source": '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>',
        "text": "Keep up the great work, MSNBC! \ud83d\udc4d https://t.co/eLAGZdirf9",
        "urls": [
            Url(
                **{
                    "expanded_url": "https://twitter.com/kenklippenstein/status/1218638650726146050",
                    "url": "https://t.co/eLAGZdirf9",
                }
            )
        ],
        "user": User(
            **{
                "created_at": "Mon Sep 01 03:13:32 +0000 2008",
                "description": "Journalist @TheIntercept; author, No Place to Hide; animal fanatic; HOPE (https://t.co/RTpovVrBZ0); vegan; IG: Glenn.11.Greenwald",
                "favourites_count": 5120,
                "followers_count": 1421166,
                "following": True,
                "friends_count": 993,
                "id": 16076032,
                "id_str": "16076032",
                "listed_count": 20858,
                "name": "Glenn Greenwald",
                "profile_background_color": "C0DEED",
                "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
                "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
                "profile_banner_url": "https://pbs.twimg.com/profile_banners/16076032/1552437882",
                "profile_image_url": "http://pbs.twimg.com/profile_images/1092582027994509312/cpYWuYI9_normal.jpg",
                "profile_image_url_https": "https://pbs.twimg.com/profile_images/1092582027994509312/cpYWuYI9_normal.jpg",
                "profile_link_color": "0084B4",
                "profile_sidebar_border_color": "000000",
                "profile_sidebar_fill_color": "000000",
                "profile_text_color": "000000",
                "screen_name": "ggreenwald",
                "statuses_count": 64887,
                "url": "https://t.co/uIEpel7tjt",
                "verified": True,
            }
        ),
        "user_mentions": [],
    }
)
mock_status: List[Status] = [
    Status(
        **{
            "created_at": "Sun Jan 19 03:36:13 +0000 2020",
            "hashtags": [],
            "id": 1218738908479008769,
            "id_str": "1218738908479008769",
            "in_reply_to_screen_name": "PatTheBerner",
            "in_reply_to_status_id": 1218738528605163521,
            "in_reply_to_user_id": 816578053627252740,
            "lang": "en",
            "media": [
                {
                    "display_url": "pic.twitter.com/7cR3xygsNw",
                    "expanded_url": "https://twitter.com/FTBandFTR/status/1218738908479008769/photo/1",
                    "id": 1218738907149414400,
                    "media_url": "http://pbs.twimg.com/media/EOnUlDKWsAA8DL7.png",
                    "media_url_https": "https://pbs.twimg.com/media/EOnUlDKWsAA8DL7.png",
                    "sizes": {
                        "large": {"h": 677, "resize": "fit", "w": 640},
                        "medium": {"h": 677, "resize": "fit", "w": 640},
                        "small": {"h": 677, "resize": "fit", "w": 640},
                        "thumb": {"h": 150, "resize": "crop", "w": 150},
                    },
                    "type": "photo",
                    "url": "https://t.co/7cR3xygsNw",
                }
            ],
            "source": "<a href='http://dadgumsalsa.com' rel='nofollow'>DadGumPiBot</a>",
            "text": "@PatTheBerner This Tweet is available! \\nFor the blocked and the record!\\nURL(s) from tweet: https://t.co/9Qpdnfytjq https://t.co/7cR3xygsNw",
            "urls": [
                {
                    "expanded_url": "https://twitter.com/i/web/status/1218686902011711488",
                    "url": "https://t.co/9Qpdnfytjq",
                }
            ],
            "user": {
                "created_at": "Thu Mar 16 01:37:58 +0000 2017",
                "default_profile": True,
                "description": "If someone wants off the list that\\u2019s okay. I will remove them ASAP. This account auto screen caps tweets that are quoted by select users I @_b_axe follow.",
                "favourites_count": 14,
                "followers_count": 32,
                "friends_count": 13,
                "id": 842188154698399746,
                "id_str": "842188154698399746",
                "location": "Austin, TX",
                "name": "For the blocked and For the record",
                "profile_background_color": "F5F8FA",
                "profile_image_url": "http://pbs.twimg.com/profile_images/1195922003615727617/hhgc1XSp_normal.jpg",
                "profile_image_url_https": "https://pbs.twimg.com/profile_images/1195922003615727617/hhgc1XSp_normal.jpg",
                "profile_link_color": "1DA1F2",
                "profile_sidebar_border_color": "C0DEED",
                "profile_sidebar_fill_color": "DDEEF6",
                "profile_text_color": "333333",
                "profile_use_background_image": True,
                "screen_name": "FTBandFTR",
                "statuses_count": 2575,
            },
            "user_mentions": [
                {
                    "id": 816578053627252740,
                    "id_str": "816578053627252740",
                    "name": "Pat the Berner\\ud83c\\udf39",
                    "screen_name": "PatTheBerner",
                }
            ],
        }
    )
]
