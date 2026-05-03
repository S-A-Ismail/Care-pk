/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [],
  },

  webpack: (config) => {
    // Docker on Windows/Mac uses a virtual filesystem for volume mounts.
    // The default inotify file-watcher doesn't receive change events across
    // that boundary, so hot reload silently breaks. Polling every 1 s fixes it.
    // aggregateTimeout batches rapid successive changes into one rebuild.
    config.watchOptions = { poll: 1000, aggregateTimeout: 300 };
    return config;
  },
};

export default nextConfig;
