var sourcesIndex = JSON.parse('{\
"document_metrics":["",[],["main.rs"]],\
"generate_schema":["",[],["main.rs"]],\
"process_event":["",[],["main.rs"]],\
"relay":["",[],["cli.rs","cliapp.rs","main.rs","setup.rs","utils.rs"]],\
"relay_auth":["",[],["lib.rs"]],\
"relay_aws_extension":["",[],["aws_extension.rs","lib.rs"]],\
"relay_cabi":["",[],["auth.rs","constants.rs","core.rs","ffi.rs","lib.rs","processing.rs"]],\
"relay_common":["",[],["constants.rs","glob.rs","lib.rs","macros.rs","project.rs","time.rs"]],\
"relay_config":["",[],["byte_size.rs","config.rs","lib.rs","upstream.rs"]],\
"relay_crash":["",[],["lib.rs"]],\
"relay_dynamic_config":["",[],["error_boundary.rs","feature.rs","lib.rs","metrics.rs","project.rs","utils.rs"]],\
"relay_ffi":["",[],["lib.rs"]],\
"relay_ffi_macros":["",[],["lib.rs"]],\
"relay_filter":["",[],["browser_extensions.rs","client_ips.rs","common.rs","config.rs","csp.rs","error_messages.rs","legacy_browsers.rs","lib.rs","localhost.rs","releases.rs","web_crawlers.rs"]],\
"relay_general":["",[["pii",[],["attachments.rs","builtin.rs","compiledconfig.rs","config.rs","convert.rs","generate_selectors.rs","legacy.rs","minidumps.rs","mod.rs","processor.rs","redactions.rs","regexes.rs","utils.rs"]],["processor",[],["attrs.rs","chunks.rs","funcs.rs","impls.rs","mod.rs","selector.rs","size.rs","traits.rs"]],["protocol",[["contexts",[],["app.rs","browser.rs","cloud_resource.rs","device.rs","gpu.rs","mod.rs","monitor.rs","os.rs","otel.rs","profile.rs","reprocessing.rs","response.rs","runtime.rs","trace.rs"]]],["breadcrumb.rs","breakdowns.rs","client_report.rs","clientsdk.rs","constants.rs","debugmeta.rs","event.rs","exception.rs","fingerprint.rs","logentry.rs","measurements.rs","mechanism.rs","metrics.rs","mod.rs","relay_info.rs","replay.rs","request.rs","schema.rs","security_report.rs","session.rs","span.rs","stacktrace.rs","tags.rs","templateinfo.rs","thread.rs","transaction.rs","types.rs","user.rs","user_report.rs","utils.rs"]],["store",[["normalize",[],["breakdowns.rs","contexts.rs","logentry.rs","mechanism.rs","request.rs","spans.rs","stacktrace.rs","user_agent.rs"]],["transactions",[],["mod.rs","processor.rs","rules.rs"]]],["clock_drift.rs","event_error.rs","geo.rs","legacy.rs","mod.rs","normalize.rs","regexes.rs","remove_other.rs","schema.rs","trimming.rs"]],["types",[],["annotated.rs","impls.rs","meta.rs","mod.rs","span_attributes.rs","traits.rs","value.rs"]]],["lib.rs","macros.rs","user_agent.rs","utils.rs"]],\
"relay_general_derive":["",[],["empty.rs","jsonschema.rs","lib.rs","process.rs"]],\
"relay_kafka":["",[["producer",[],["mod.rs","utils.rs"]]],["config.rs","lib.rs","statsd.rs"]],\
"relay_log":["",[],["lib.rs","setup.rs","test.rs","utils.rs"]],\
"relay_metrics":["",[],["aggregation.rs","lib.rs","protocol.rs","statsd.rs"]],\
"relay_profiling":["",[],["android.rs","cocoa.rs","error.rs","lib.rs","measurements.rs","native_debug_image.rs","outcomes.rs","sample.rs","transaction_metadata.rs","utils.rs"]],\
"relay_quotas":["",[],["lib.rs","quota.rs","rate_limit.rs","redis.rs"]],\
"relay_redis":["",[],["config.rs","lib.rs","real.rs"]],\
"relay_replays":["",[],["lib.rs","recording.rs","transform.rs"]],\
"relay_sampling":["",[],["lib.rs"]],\
"relay_server":["",[["actors",[],["envelopes.rs","health_check.rs","mod.rs","outcome.rs","outcome_aggregator.rs","processor.rs","project.rs","project_cache.rs","project_local.rs","project_redis.rs","project_upstream.rs","relays.rs","server.rs","store.rs","test_store.rs","upstream.rs"]],["body",[],["mod.rs","peek_line.rs","request_body.rs","store_body.rs"]],["endpoints",[],["attachments.rs","common.rs","envelope.rs","events.rs","forward.rs","health_check.rs","minidump.rs","mod.rs","outcomes.rs","project_configs.rs","public_keys.rs","security_report.rs","statics.rs","store.rs","unreal.rs"]],["extractors",[],["decoder.rs","forwarded_for.rs","mod.rs","request_meta.rs","shared_payload.rs","signed_json.rs","start_time.rs"]],["metrics_extraction",[],["conditional_tagging.rs","mod.rs","sessions.rs","transactions.rs","utils.rs"]],["utils",[],["api.rs","buffer.rs","dynamic_sampling.rs","envelope_context.rs","garbage.rs","metrics_rate_limits.rs","mod.rs","multipart.rs","native.rs","param_parser.rs","rate_limits.rs","request.rs","retry.rs","semaphore.rs","sizes.rs","sleep_handle.rs","unreal.rs"]]],["constants.rs","envelope.rs","http.rs","lib.rs","middlewares.rs","service.rs","statsd.rs"]],\
"relay_statsd":["",[],["lib.rs"]],\
"relay_system":["",[],["controller.rs","lib.rs","service.rs","statsd.rs"]],\
"relay_test":["",[],["lib.rs"]],\
"scrub_minidump":["",[],["main.rs"]]\
}');
createSourceSidebar();
