# Unique ELBv2 Listener Rule Priority

Without any conflict, generate random priotity for a Elastic Load Balancer
Listener Rule.

## Usage

### Produce only one priority

```yaml
      - uses: licenseware/unique-elbv2-listener-rule-priority@v1
        id: elb-priority
        with:
          listener-arn: ${{ secrets.LOAD_BALANCER_LISTENER_ARN }}

      - uses: aws-actions/aws-cloudformation-github-deploy@v1
        with:
          name: sample-elb-priority
          template: cloudformation-templates/myapp-dev.yml
          no-fail-on-empty-changeset: "1"
          role-arn: ${{ secrets.CLOUD_FORMATION_ROLE_ARN }}
          parameter-overrides: >-
            MyAppLBPriority=${{ steps.elb-priority.outputs.prioritties }}
```

### Produce multiple priorities

```yaml
      - uses: licenseware/unique-elbv2-listener-rule-priority@v1
        id: elb-priority
        with:
          listener-arn: ${{ secrets.LOAD_BALANCER_LISTENER_ARN }}
          count: 3

      - uses: aws-actions/aws-cloudformation-github-deploy@v1
        with:
          name: sample-elb-priority
          template: cloudformation-templates/myapp-dev.yml
          no-fail-on-empty-changeset: "1"
          role-arn: ${{ secrets.CLOUD_FORMATION_ROLE_ARN }}
          parameter-overrides: >-
            MyAppLBPriority=${{ steps.elb-priority.outputs.prioritties | cut -d',' -f1 }},
            YourAppLBPriority=${{ steps.elb-priority.outputs.prioritties | cut -d',' -f2 }}},
            HisAppLBPriority=${{ steps.elb-priority.outputs.prioritties | cut -d',' -f3 }}
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| listener-arn | The ARN of the ELBv2 Listener to generate the priority for. | true |
| count | The number of priorities to generate. | false | 1 |
| min-priority | The minimum priority to use. | false | 1 |
| max-priority | The maximum priority to use. | false | 50000 |
| max-try | The maximum number of tries to generate a unique priority. | false | 10000 |
| log-level | The log level to use. | false | error |


## Outputs

| Name | Description | Example |
|------|-------------|---------|
| prioritties | Comma-separated list of generated priorities. | 1,2,3 |
