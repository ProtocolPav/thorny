# Thorny 🤖

**A Discord bot for the Everthorn Community, by the Everthorn Community.**

Thorny brings fun, engagement, and utility to the Everthorn Discord server with easy setup and community-focused features.

---

## 🚀 Getting Started

You can run Thorny either by building the Docker image locally or by pulling a prebuilt image from a registry.

### 1️⃣ Build & Run Locally

```bash
# Build the Docker image
docker build -t thorny ./thorny

# Run the container
docker run -d --name thorny -e BOT_TOKEN=<DISCORD_BOT_TOKEN> -e GIPHY_TOKEN=<GIPHY_API_TOKEN> thorny
```

### 2️⃣ Using Docker Compose

Here’s a basic `docker-compose.yml` example:

```yaml
version: '3.8'
services:
  thorny:
    # Build locally
    build: ./thorny
    
    # Or use a prebuilt image
    # image: <YOUR_IMAGE_URL>
    
    # Used for development purposes
    # volumes:
    #   - ./thorny/:/thorny_core/
    container_name: 'thorny'
    environment:
      - BOT_TOKEN=<DISCORD_BOT_TOKEN>
      - GIPHY_TOKEN=<GIPHY_API_TOKEN>
```

Run it with:

```bash
docker-compose up -d
```

---

## ⚙️ Configuration

| Environment Variable | Description                     |
| -------------------- | ------------------------------- |
| `BOT_TOKEN`          | Your Discord bot token          |
| `GIPHY_TOKEN`        | Your Giphy API token (optional) |

---

## 📝 Notes

* Thorny is designed for the Everthorn community but can be adapted for other servers.
* Make sure your bot has the necessary permissions in Discord to read messages and respond.

---

## 💡 Contributing

We love contributions! Feel free to open issues or submit pull requests to improve Thorny.
