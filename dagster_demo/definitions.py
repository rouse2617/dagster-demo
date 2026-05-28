from dagster import Definitions
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

dagster_demo_project = DbtProject(project_dir=".")
dagster_demo_project.prepare_if_dev()


@dbt_assets(manifest=dagster_demo_project.manifest_path)
def dagster_demo_assets(context):
    yield from (
        DbtCliResource(project_dir=".")
        .cli(["build"], context=context)
        .stream()
    )


defs = Definitions(assets=[dagster_demo_assets])
