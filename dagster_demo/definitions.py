from dagster import Definitions, load_assets_from_modules

from dagster_demo.assets import sales_analytics

all_assets = load_assets_from_modules([sales_analytics])

defs = Definitions(assets=all_assets)
