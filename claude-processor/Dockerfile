FROM debian:bookworm

# Install essential packages
RUN apt-get update && apt-get install -y \
    build-essential autoconf automake cmake git \
    python3-dev python3-venv python3-pip \
    nodejs npm \
    bash tmux \
    openssh-server \
    wget curl \
    ca-certificates \
    sudo \
    nano vim neovim \
    ripgrep \
    rclone \
    && rm -rf /var/lib/apt/lists/*

# Create SSH directory and configure SSH
#RUN mkdir /var/run/sshd && \
#    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
#    sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

# Create a non-root user for development
RUN useradd -m -s /bin/bash developer && \
    echo "developer:developer" | chpasswd && \
    usermod -aG sudo developer

# Switch to developer user to install Claude Code
USER developer
WORKDIR /home/developer

# Install Claude Code using the native installer
RUN curl -fsSL https://claude.ai/install.sh | bash && \
    echo 'export PATH="$HOME/.claude/bin:$PATH"' >> ~/.bashrc

# Switch back to root for SSH setup
USER root

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]