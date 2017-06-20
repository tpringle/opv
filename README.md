# opv
The Octopus Project Validator

## Outline

If you've been using Octopus Deploy in a large scale environment for any amount of time you would of run into scenarios when project configuration has somehow drifted from its original definition.
Maybe developers have introduced some weird settings, maybe a variable set wasn't attached to a project. Who Knows?

Regardless of what it is we all need a simple way to check that our projects are configured as we desire.

That is why this project was created.

By defining which configuration settings you wish to check within the `checks.toml` file, the `opv` tool will scan through all of your projects and advise you of any incorrect configurations.

You can think of this tool as an Operational Validator for Octopus Deploy Projects.

## Checks

Checks are super easy to make!

The definitions are based on the names and values found on the Octopus Projects API `(/api/projects)`.

Reading through this API page after page is not very practical when you're trying to find a mis-configuration.

See the example `checks.toml` file in this repository to get started.

A basic set of checks would be defined like so:

```
[server]
url = "https://octopus-deploy.mydomain.com" #this is required

[checks]
ProjectConnectivityPolicy = { SkipMachineBehavior = "SkipUnavailableMachines", AllowDeploymentsToNoTargets = false }
IncludedLibraryVariableSetIds = ["LibraryVariableSets-124", "LibraryVariableSets-21"]
IsDisabled = false
TenantedDeploymentMode = "Untenanted"
```

The Server url is required in order for `opv` to connect to your projects api.
Checks are created in a Key/Value type approach following standard toml syntax.

## Installation

`pip install -r requirements.txt`

## Usage

`python main.py --apikey API-XXXXKEYXXXX`
