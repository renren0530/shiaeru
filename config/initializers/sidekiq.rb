Sidekiq.configure_server do |config|
  config.redis = { url: 'http://proxy:29ffa8b9ae0842c7b0a1398b4ed26f28@proxy-54-225-208-216.proximo.io' }
end

Sidekiq.configure_client do |config|
  config.redis = { url: 'http://proxy:29ffa8b9ae0842c7b0a1398b4ed26f28@proxy-54-225-208-216.proximo.io' }
end