DROP TABLE IF EXISTS cdm.user_product_counters CASCADE;
CREATE TABLE IF NOT EXISTS cdm.user_product_counters
(
    id              INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id         UUID NOT NULL,
    product_id      UUID NOT NULL,
    product_name    VARCHAR NOT NULL,
    order_cnt       INT DEFAULT 0 NOT NULL CHECK (order_cnt >= 0),
    CONSTRAINT user_product_counters_unq UNIQUE(user_id, product_id)
);

DROP TABLE IF EXISTS cdm.user_category_counters CASCADE;
CREATE TABLE IF NOT EXISTS cdm.user_category_counters
(
    id              INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id         UUID NOT NULL,
    category_id     UUID NOT NULL,
    category_name   VARCHAR NOT NULL,
    order_cnt       INT DEFAULT 0 NOT NULL CHECK (order_cnt >= 0),
    CONSTRAINT user_category_counters_unq UNIQUE(user_id, category_id)
);

DROP TABLE IF EXISTS stg.order_events CASCADE;
CREATE TABLE IF NOT EXISTS stg.order_events
(
    id              INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    object_id       INT UNIQUE NOT NULL,
    object_type     VARCHAR NOT NULL,
    sent_dttm       TIMESTAMP NOT NULL,
    payload         JSON NOT NULL
);

DROP TABLE IF EXISTS dds.h_user CASCADE;
CREATE TABLE IF NOT EXISTS dds.h_user
(
    h_user_pk       UUID NOT NULL PRIMARY KEY,
    user_id         VARCHAR NOT NULL,
    load_dt         TIMESTAMP NOT NULL,
    load_src        VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.h_product CASCADE;
CREATE TABLE IF NOT EXISTS dds.h_product
(
    h_product_pk    UUID NOT NULL PRIMARY KEY,
    product_id      VARCHAR NOT NULL,
    load_dt         TIMESTAMP NOT NULL,
    load_src        VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.h_category CASCADE;
CREATE TABLE IF NOT EXISTS dds.h_category
(
    h_category_pk   UUID NOT NULL PRIMARY KEY,
    category_name   VARCHAR NOT NULL,
    load_dt         TIMESTAMP NOT NULL,
    load_src        VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.h_restaurant CASCADE;
CREATE TABLE IF NOT EXISTS dds.h_restaurant
(
    h_restaurant_pk UUID NOT NULL PRIMARY KEY,
    restaurant_id   VARCHAR NOT NULL,
    load_dt         TIMESTAMP NOT NULL,
    load_src        VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.h_order CASCADE;
CREATE TABLE IF NOT EXISTS dds.h_order
(
    h_order_pk      UUID NOT NULL PRIMARY KEY,
    order_id        INT NOT NULL,
    order_dt        TIMESTAMP NOT NULL,
    load_dt         TIMESTAMP NOT NULL,
    load_src        VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.l_order_product CASCADE;
CREATE TABLE IF NOT EXISTS dds.l_order_product
(
    hk_order_product_pk UUID UNIQUE NOT NULL PRIMARY KEY,
    h_order_pk          UUID NOT NULL CONSTRAINT fk_l_order_product_order REFERENCES dds.h_order(h_order_pk),
    h_product_pk        UUID NOT NULL CONSTRAINT fk_l_order_product_product REFERENCES dds.h_product(h_product_pk),
    load_dt             TIMESTAMP NOT NULL,
    load_src            VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.l_product_restaurant CASCADE;
CREATE TABLE IF NOT EXISTS dds.l_product_restaurant
(
    hk_product_restaurant_pk UUID UNIQUE NOT NULL PRIMARY KEY,
    h_product_pk             UUID NOT NULL CONSTRAINT fk_l_product_restaurant_product REFERENCES dds.h_product(h_product_pk),
    h_restaurant_pk          UUID NOT NULL CONSTRAINT fk_l_product_restaurant_restaurant REFERENCES dds.h_restaurant(h_restaurant_pk),
    load_dt                  TIMESTAMP NOT NULL,
    load_src                 VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.l_product_category CASCADE;
CREATE TABLE IF NOT EXISTS dds.l_product_category
(
    hk_product_category_pk   UUID UNIQUE NOT NULL PRIMARY KEY,
    h_product_pk             UUID NOT NULL CONSTRAINT fk_l_product_category_product REFERENCES dds.h_product(h_product_pk),
    h_category_pk            UUID NOT NULL CONSTRAINT fk_l_product_category_category REFERENCES dds.h_category(h_category_pk),
    load_dt                  TIMESTAMP NOT NULL,
    load_src                 VARCHAR NOT NULL
);


DROP TABLE IF EXISTS dds.l_order_user CASCADE;
CREATE TABLE IF NOT EXISTS dds.l_order_user
(
    hk_order_user_pk         UUID UNIQUE NOT NULL PRIMARY KEY,
    h_order_pk               UUID NOT NULL CONSTRAINT fk_l_order_user_order REFERENCES dds.h_order(h_order_pk),
    h_user_pk                UUID NOT NULL CONSTRAINT fk_l_order_user_user REFERENCES dds.h_user(h_user_pk),
    load_dt                  TIMESTAMP NOT NULL,
    load_src                 VARCHAR NOT NULL
);


DROP TABLE IF EXISTS dds.s_user_names CASCADE;
CREATE TABLE IF NOT EXISTS dds.s_user_names
(
    hk_user_names_hashdiff  UUID UNIQUE NOT NULL PRIMARY KEY,
    h_user_pk               UUID NOT NULL CONSTRAINT fk_s_user_names_user REFERENCES dds.h_user(h_user_pk),
    username                VARCHAR NOT NULL,
    userlogin               VARCHAR NOT NULL,
    load_dt                 TIMESTAMP NOT NULL,
    load_src                VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.s_product_names CASCADE;
CREATE TABLE IF NOT EXISTS dds.s_product_names
(
    hk_product_names_hashdiff  UUID UNIQUE NOT NULL PRIMARY KEY,
    h_product_pk               UUID NOT NULL CONSTRAINT fk_s_product_names_product REFERENCES dds.h_product(h_product_pk),
    name                       VARCHAR NOT NULL,
    load_dt                    TIMESTAMP NOT NULL,
    load_src                   VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.s_restaurant_names CASCADE;
CREATE TABLE IF NOT EXISTS dds.s_restaurant_names
(
    hk_restaurant_names_hashdiff  UUID UNIQUE NOT NULL PRIMARY KEY,
    h_restaurant_pk               UUID NOT NULL CONSTRAINT fk_s_restaurant_names_restaurant REFERENCES dds.h_restaurant(h_restaurant_pk),
    name                          VARCHAR NOT NULL,
    load_dt                       TIMESTAMP NOT NULL,
    load_src                      VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.s_order_cost CASCADE;
CREATE TABLE IF NOT EXISTS dds.s_order_cost
(
    hk_order_cost_hashdiff        UUID UNIQUE NOT NULL PRIMARY KEY,
    h_order_pk                    UUID NOT NULL CONSTRAINT fk_s_order_cost_order REFERENCES dds.h_order(h_order_pk),
    "cost"                        DECIMAL(19, 5) NOT NULL CHECK ("cost" >= 0),
    payment                       DECIMAL(19, 5) NOT NULL CHECK (payment >= 0),
    load_dt                       TIMESTAMP NOT NULL,
    load_src                      VARCHAR NOT NULL
);

DROP TABLE IF EXISTS dds.s_order_status CASCADE;
CREATE TABLE IF NOT EXISTS dds.s_order_status
(
    hk_order_status_hashdiff      UUID UNIQUE NOT NULL PRIMARY KEY,
    h_order_pk                    UUID NOT NULL CONSTRAINT fk_s_order_status_order REFERENCES dds.h_order(h_order_pk),
    status                        VARCHAR NOT NULL,
    load_dt                       TIMESTAMP NOT NULL,
    load_src                      VARCHAR NOT NULL
);