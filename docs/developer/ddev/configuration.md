# Configuration

-----

All configuration can be managed entirely by the `ddev config` command group. To locate the global
[TOML][toml-github] config file, run:

```
ddev config find
```

!!! info "Config overrides"
    When running `ddev`, if the current working directory (or a parent directory) contains a `.ddev.toml` file, any options defined in this file will override those in the global
    configuration file. This allows easy configuration sets depending on the working directory `ddev` is run from.
    See the [Multi-repo/Worktrees](multirepo.md) documentation for more details on how overrides work and affect commands.

## Repository

All CLI commands are aware of the current repository context, defined by the option `repo`. This option should be a
reference to a key in `repos` which is set to the path of a supported repository. For example, this configuration:

```toml
repo = "core"

[repos]
core = "/path/to/integrations-core"
extras = "/path/to/integrations-extras"
agent = "/path/to/datadog-agent"
```

would make it so running e.g. `ddev test nginx` will look for an integration named `nginx` in `/path/to/integrations-core`
no matter what directory you are in. If the selected path does not exist, then the current directory will be used.

By default, `repo` is set to `core`. To easily switch between repositories depending on your current directory take a look at how to work with [Multi-repo/Worktrees](multirepo.md).

## Agent

For running environments with a [live Agent](../e2e.md), you can select a specific build version to use with the
option `agent`. This option should be a reference to a key in `agents` which is a mapping of environment types to
Agent versions. For example, this configuration:

```toml
agent = "master"

[agents.master]
docker = "datadog/agent-dev:master"
local = "latest"

[agents."7.18.1"]
docker = "datadog/agent:7.18.1"
local = "7.18.1"
```

would make it so environments that [define](plugins.md#metadata) the type as `docker` will use the Docker image
that was built with the latest commit to the [datadog-agent][] repo.

## Organization

You can switch to using a particular organization with the option `org`. This option should be a reference to a
key in `orgs` which is a mapping containing data specific to the organization. For example, this configuration:

```toml
org = "staging"

[orgs.staging]
api_key = "<API_KEY>"
app_key = "<APP_KEY>"
site = "datadoghq.eu"
```

would use the access keys for the organization named `staging` and would submit data to the EU region.

The supported fields are:

- [api_key][datadog-config-api-key]
- [app_key][datadog-config-app-key]
- [site][datadog-config-site]
- [dd_url][datadog-config-dd-url]
- [log_url][datadog-config-log-url]

## GitHub

To avoid GitHub's public API rate limits, you need to set `github.user`/`github.token` in your config file or
use the `DD_GITHUB_USER`/`DD_GITHUB_TOKEN` environment variables.

Run `ddev config show` to see if your GitHub user and token is set.

If not:

1. Run `ddev config set github.user <YOUR_GITHUB_USERNAME>`
1. Create a [personal access token][github-personal-access-token] with `public_repo` and `read:org` permissions
1. Run `ddev config set github.token` then paste the token
1. [Enable single sign-on][github-saml-single-sign-on] for the token
