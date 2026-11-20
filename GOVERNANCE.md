# Governance

[Español](GOVERNANCE.es.md)

## Two levels

**1. The method (this repository).** story-forge's methodology belongs to its author, David Dávila, who maintains this repository and decides what enters the shared version: skills, templates, the starter knowledge base and the documentation. Anyone can propose changes through issues and pull requests (see [CONTRIBUTING.md](CONTRIBUTING.md)); the maintainer reviews and merges them.

**2. Each implementation (your team).** Every Product Owner can change their own implementation without asking anyone: the team profile, the knowledge base (writing rules and standard behaviors), the templates and, if needed, a fork of the skills. The only limit is your organization: if its policies require approval for standards, templates or tools, those policies come first.

## How the plugin applies it

The team profile has a `governance` section:

```yaml
governance:
  kb_changes: po               # po = the Product Owner approves | organization = needs the approval named below
  approver: ""                 # role or group that approves when kb_changes is organization
```

- With `po` (default), `sf-retro` and `sf-setup` ask the Product Owner and apply what they approve.
- With `organization`, they prepare the proposal (rule text, evidence, affected page) for the named approver and change nothing until the Product Owner confirms that it was approved.
- In both cases, changes are written only to the knowledge base of the market they belong to.

## Sharing improvements back

If a change in your implementation would help other teams, propose it upstream without company data: generic wording, invented examples, no names of clients, systems or people. Rules accepted upstream join the starter set with origin "Community".

## Licence

Apache License 2.0. You may use, modify and redistribute the method under its terms, keeping the attribution in [NOTICE](NOTICE).
