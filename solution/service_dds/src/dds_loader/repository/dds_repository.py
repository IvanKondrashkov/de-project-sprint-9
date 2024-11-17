from uuid import UUID
from datetime import datetime
from lib.pg import PgConnect

class DdsRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db  

    def h_user_insert(self,
                      h_user_pk: UUID,
                      user_id: str,
                      load_dt: datetime,
                      load_src: str
                      ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_user(h_user_pk, user_id, load_dt, load_src)
                        VALUES (%(h_user_pk)s, %(user_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_user_pk) DO UPDATE
                        SET
                            user_id = EXCLUDED.user_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_user_pk': h_user_pk,
                        'user_id': user_id,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def h_product_insert(self,
                         h_product_pk: UUID,
                         product_id: str,
                         load_dt: datetime,
                         load_src: str
                         ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_product(h_product_pk, product_id, load_dt, load_src)
                        VALUES (%(h_product_pk)s, %(product_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_product_pk) DO UPDATE
                        SET
                            product_id = EXCLUDED.product_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_product_pk': h_product_pk,
                        'product_id': product_id,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def h_category_insert(self,
                          h_category_pk: UUID,
                          category_name: str,
                          load_dt: datetime,
                          load_src: str
                          ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_category(h_category_pk, category_name, load_dt, load_src)
                        VALUES (%(h_category_pk)s, %(category_name)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_category_pk) DO UPDATE
                        SET
                            category_name = EXCLUDED.category_name,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_category_pk': h_category_pk,
                        'category_name': category_name,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def h_restaurant_insert(self,
                            h_restaurant_pk: UUID,
                            restaurant_id: str,
                            load_dt: datetime,
                            load_src: str
                            ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_restaurant(h_restaurant_pk, restaurant_id, load_dt, load_src)
                        VALUES (%(h_restaurant_pk)s, %(restaurant_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_restaurant_pk) DO UPDATE
                        SET
                            restaurant_id = EXCLUDED.restaurant_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_restaurant_pk': h_restaurant_pk,
                        'restaurant_id': restaurant_id,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def h_order_insert(self,
                       h_order_pk: UUID,
                       order_id: int,
                       order_dt: datetime,
                       load_dt: datetime,
                       load_src: str
                       ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_order(h_order_pk, order_id, order_dt, load_dt, load_src)
                        VALUES (%(h_order_pk)s, %(order_id)s, %(order_dt)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_order_pk) DO UPDATE
                        SET
                            order_id = EXCLUDED.order_id,
                            order_dt = EXCLUDED.order_dt,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_order_pk': h_order_pk,
                        'order_id': order_id,
                        'order_dt': order_dt,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def l_order_product_insert(self,
                               hk_order_product_pk: UUID,
                               h_order_pk: UUID,
                               h_product_pk: UUID,
                               load_dt: datetime,
                               load_src: str
                               ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_order_product(hk_order_product_pk, h_order_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_order_product_pk)s, %(h_order_pk)s, %(h_product_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_order_product_pk) DO UPDATE
                        SET
                            h_order_pk = EXCLUDED.h_order_pk,
                            h_product_pk = EXCLUDED.h_product_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_order_product_pk': hk_order_product_pk,
                        'h_order_pk': h_order_pk,
                        'h_product_pk': h_product_pk,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def l_product_restaurant_insert(self,
                                    hk_product_restaurant_pk: UUID,
                                    h_product_pk: UUID,
                                    h_restaurant_pk: UUID,
                                    load_dt: datetime,
                                    load_src: str
                                    ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_product_restaurant(hk_product_restaurant_pk, h_product_pk, h_restaurant_pk, load_dt, load_src)
                        VALUES (%(hk_product_restaurant_pk)s, %(h_product_pk)s, %(h_restaurant_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_product_restaurant_pk) DO UPDATE
                        SET
                            h_product_pk = EXCLUDED.h_product_pk,
                            h_restaurant_pk = EXCLUDED.h_restaurant_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_product_restaurant_pk': hk_product_restaurant_pk,
                        'h_product_pk': h_product_pk,
                        'h_restaurant_pk': h_restaurant_pk,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def l_product_category_insert(self,
                                  hk_product_category_pk: UUID,
                                  h_product_pk: UUID,
                                  h_category_pk: UUID,
                                  load_dt: datetime,
                                  load_src: str
                                  ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_product_category(hk_product_category_pk, h_product_pk, h_category_pk, load_dt, load_src)
                        VALUES (%(hk_product_category_pk)s, %(h_product_pk)s, %(h_category_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_product_category_pk) DO UPDATE
                        SET
                            h_product_pk = EXCLUDED.h_product_pk,
                            h_category_pk = EXCLUDED.h_category_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_product_category_pk': hk_product_category_pk,
                        'h_product_pk': h_product_pk,
                        'h_category_pk': h_category_pk,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def l_order_user_insert(self,
                            hk_order_user_pk: UUID,
                            h_order_pk: UUID,
                            h_user_pk: UUID,
                            load_dt: datetime,
                            load_src: str
                            ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_order_user(hk_order_user_pk, h_order_pk, h_user_pk, load_dt, load_src)
                        VALUES (%(hk_order_user_pk)s, %(h_order_pk)s, %(h_user_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_order_user_pk) DO UPDATE
                        SET
                            h_order_pk = EXCLUDED.h_order_pk,
                            h_user_pk = EXCLUDED.h_user_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_order_user_pk': hk_order_user_pk,
                        'h_order_pk': h_order_pk,
                        'h_user_pk': h_user_pk,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def s_user_names_insert(self,
                            hk_user_names_hashdiff: UUID,
                            h_user_pk: UUID,
                            username: str,
                            userlogin: str,
                            load_dt: datetime,
                            load_src: str
                            ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_user_names(hk_user_names_hashdiff, h_user_pk, username, userlogin, load_dt, load_src)
                        VALUES (%(hk_user_names_hashdiff)s, %(h_user_pk)s, %(username)s, %(userlogin)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_user_names_hashdiff) DO UPDATE
                        SET
                            h_user_pk = EXCLUDED.h_user_pk,
                            username = EXCLUDED.username,
                            userlogin = EXCLUDED.userlogin,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_user_names_hashdiff': hk_user_names_hashdiff,
                        'h_user_pk': h_user_pk,
                        'username': username,
                        'userlogin': userlogin,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def s_product_names_insert(self,
                               hk_product_names_hashdiff: UUID,
                               h_product_pk: UUID,
                               name: str,
                               load_dt: datetime,
                               load_src: str
                               ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_product_names(hk_product_names_hashdiff, h_product_pk, name, load_dt, load_src)
                        VALUES (%(hk_product_names_hashdiff)s, %(h_product_pk)s, %(name)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_product_names_hashdiff) DO UPDATE
                        SET
                            h_product_pk = EXCLUDED.h_product_pk,
                            name = EXCLUDED.name,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_product_names_hashdiff': hk_product_names_hashdiff,
                        'h_product_pk': h_product_pk,
                        'name': name,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def s_restaurant_names_insert(self,
                                  hk_restaurant_names_hashdiff: UUID,
                                  h_restaurant_pk: UUID,
                                  name: str,
                                  load_dt: datetime,
                                  load_src: str
                                  ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_restaurant_names(hk_restaurant_names_hashdiff, h_restaurant_pk, name, load_dt, load_src)
                        VALUES (%(hk_restaurant_names_hashdiff)s, %(h_restaurant_pk)s, %(name)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_restaurant_names_hashdiff) DO UPDATE
                        SET
                            h_restaurant_pk = EXCLUDED.h_restaurant_pk,
                            name = EXCLUDED.name,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_restaurant_names_hashdiff': hk_restaurant_names_hashdiff,
                        'h_restaurant_pk': h_restaurant_pk,
                        'name': name,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def s_order_cost_insert(self,
                            hk_order_cost_hashdiff: UUID,
                            h_order_pk: UUID,
                            cost: float,
                            payment: float,
                            load_dt: datetime,
                            load_src: str
                            ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_order_cost(hk_order_cost_hashdiff, h_order_pk, cost, payment, load_dt, load_src)
                        VALUES (%(hk_order_cost_hashdiff)s, %(h_order_pk)s, %(cost)s, %(payment)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_order_cost_hashdiff) DO UPDATE
                        SET
                            h_order_pk = EXCLUDED.h_order_pk,
                            cost = EXCLUDED.cost,
                            payment = EXCLUDED.payment,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_order_cost_hashdiff': hk_order_cost_hashdiff,
                        'h_order_pk': h_order_pk,
                        'cost': cost,
                        'payment': payment,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )

    def s_order_status_insert(self,
                              hk_order_status_hashdiff: UUID,
                              h_order_pk: UUID,
                              status: str,
                              load_dt: datetime,
                              load_src: str
                              ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_order_status(hk_order_status_hashdiff, h_order_pk, status, load_dt, load_src)
                        VALUES (%(hk_order_status_hashdiff)s, %(h_order_pk)s, %(status)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_order_status_hashdiff) DO UPDATE
                        SET
                            h_order_pk = EXCLUDED.h_order_pk,
                            status = EXCLUDED.status,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_order_status_hashdiff': hk_order_status_hashdiff,
                        'h_order_pk': h_order_pk,
                        'status': status,
                        'load_dt': load_dt,
                        'load_src': load_src
                    }
                )                                                                                                                                                     