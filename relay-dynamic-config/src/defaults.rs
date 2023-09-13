use relay_base_schema::data_category::DataCategory;
use relay_common::glob2::LazyGlob;
use relay_common::glob3::GlobPatterns;
use relay_sampling::condition::{
    AndCondition, EqCondition, GlobCondition, NotCondition, RuleCondition,
};
use serde_json::Value;

use crate::feature::Feature;
use crate::metrics::{MetricExtractionConfig, MetricSpec, TagMapping, TagSpec};
use crate::project::ProjectConfig;

/// Adds configuration for extracting metrics from spans.
///
/// This configuration is temporarily hard-coded here. It will later be provided by the upstream.
/// This requires the `SpanMetricsExtraction` feature. This feature should be set to `false` if the
/// default should no longer be placed.
pub fn add_span_metrics(project_config: &mut ProjectConfig) {
    if !project_config.features.has(Feature::SpanMetricsExtraction) {
        return;
    }

    let config = project_config
        .metric_extraction
        .get_or_insert_with(MetricExtractionConfig::empty);

    if !config.is_supported() || config._span_metrics_extended {
        return;
    }

    let span_op_field_name = "span.op";
    let modules_condition = RuleCondition::And(AndCondition {
        inner: vec![
            RuleCondition::Glob(GlobCondition {
                name: span_op_field_name.into(),
                value: GlobPatterns::new(vec!["db*".into()]),
            }),
            RuleCondition::Not(NotCondition {
                inner: Box::new(RuleCondition::Eq(EqCondition {
                    name: span_op_field_name.into(),
                    value: Value::String("db.redis".into()),
                    options: Default::default(),
                })),
            }),
            RuleCondition::Not(NotCondition {
                inner: Box::new(RuleCondition::Eq(EqCondition {
                    name: span_op_field_name.into(),
                    value: Value::String("db.clickhouse".into()),
                    options: Default::default(),
                })),
            }),
            RuleCondition::Not(NotCondition {
                inner: Box::new(RuleCondition::Eq(EqCondition {
                    name: span_op_field_name.into(),
                    value: Value::String("db.sql.query".into()),
                    options: Default::default(),
                })),
            }),
        ],
    });

    config.metrics.extend([
        MetricSpec {
            category: DataCategory::Span,
            mri: "d:spans/exclusive_time@millisecond".into(),
            field: Some("span.exclusive_time".into()),
            condition: Some(modules_condition.clone()),
            tags: vec![TagSpec {
                key: "transaction".into(),
                field: Some("span.data.transaction".into()),
                value: None,
                condition: None,
            }],
        },
        MetricSpec {
            category: DataCategory::Span,
            mri: "d:spans/exclusive_time_light@millisecond".into(),
            field: Some("span.exclusive_time".into()),
            condition: Some(modules_condition.clone()),
            tags: Default::default(),
        },
    ]);

    config.tags.extend([
        TagMapping {
            metrics: vec![LazyGlob::new("d:spans/exclusive_time*@millisecond".into())],
            tags: [
                "environment",
                "http.status_code",
                "span.action",
                "span.category",
                "span.description",
                "span.domain",
                "span.group",
                "span.module",
                "span.op",
                "span.status_code",
                "span.status",
                "span.system",
                "transaction.method",
                "transaction.op",
            ]
            .map(|key| TagSpec {
                key: key.into(),
                field: Some(format!("span.data.{}", key.replace('.', "\\."))),
                value: None,
                condition: Some(modules_condition.clone()),
            })
            .into(),
        },
        TagMapping {
            metrics: vec![LazyGlob::new("d:spans/exclusive_time*@millisecond".into())],
            tags: ["release", "device.class"] // TODO: sentry PR for static strings
                .map(|key| TagSpec {
                    key: key.into(),
                    field: Some(format!("span.data.{}", key.replace('.', "\\."))),
                    value: None,
                    condition: Some(RuleCondition::And(AndCondition {
                        inner: vec![
                            RuleCondition::Eq(EqCondition {
                                name: "span.data.mobile".into(),
                                value: Value::Bool(true),
                                options: Default::default(),
                            }),
                            modules_condition.clone(),
                        ],
                    })),
                })
                .into(),
        },
    ]);

    config._span_metrics_extended = true;
    if config.version == 0 {
        config.version = MetricExtractionConfig::VERSION;
    }
}
