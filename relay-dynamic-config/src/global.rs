use std::sync::Arc;

use relay_general::store::MeasurementsConfig;
use serde::{Deserialize, Serialize};

use crate::TaggingRule;

/// A dynamic configuration for all Relays passed down from Sentry.
///
/// Values shared across all projects may also be included here, to keep
/// [`ProjectConfig`](crate::ProjectConfig)s small.
#[derive(Default, Clone, Debug, Serialize, Deserialize)]
#[serde(default, rename_all = "camelCase")]
pub struct GlobalConfig {
    /// Project configuration for measurements.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub measurements: Option<MeasurementsConfig>,
    /// Project configuration for rules for applying metrics tags depending on
    /// the event's content.
    #[serde(skip_serializing_if = "Vec::is_empty")]
    pub metric_conditional_tagging: Vec<TaggingRule>,
}

/// some docs
#[derive(Clone)]
pub enum GCState {
    ///a
    UnInit,
    ///b
    Fetched(Arc<GlobalConfig>),
}

#[cfg(test)]
mod tests {
    use crate::GlobalConfig;

    #[test]
    fn test_global_config_roundtrip() {
        let json = r#"{
  "measurements": {
    "builtinMeasurements": [
      {
        "name": "plate.size",
        "unit": "5"
      }
    ],
    "maxCustomMeasurements": 2
  },
  "metricConditionalTagging": [
    {
      "condition": {
        "op": "gt",
        "name": "food.deliciousness",
        "value": 8
      },
      "targetMetrics": [
        "tummy.satisfaction"
      ],
      "targetTag": "satisfied",
      "tagValue": "hellyeah"
    }
  ]
}"#;

        let deserialized: GlobalConfig = serde_json::from_str(json).unwrap();
        let reserialized = serde_json::to_string_pretty(&deserialized).unwrap();
        assert_eq!(json, reserialized);
    }
}
