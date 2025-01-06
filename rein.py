import torch
import torch.nn as nn
import torch.optim as optim
import gymnasium as gym
import numpy as np


class ContinuousPolicyNet(nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

        # Ortalamayı (mean) üreten katman
        self.mean_layer = nn.Linear(hidden_dim, action_dim)
        # Logaritmik varyansı (ör. diagonal) üreten katman
        self.log_std_layer = nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))

        mean = self.mean_layer(x)
        log_std = self.log_std_layer(x)
        std = torch.exp(log_std)

        return mean, std


def run_episode(env, policy_net):
    state = env.reset()[0]
    log_probs, rewards = [], []
    done = False

    while not done:
        state_tensor = torch.tensor([state], dtype=torch.float32)
        mean, std = policy_net(state_tensor)

        # Her aksiyon bileşeni için Normal dağılım
        dist = torch.distributions.Normal(mean, std)
        action = dist.sample()

        # log(π(a|s)) sakla (toplam log_prob = her aksiyon boyutuna ait log_probların toplamı)
        log_prob = dist.log_prob(action).sum(dim=-1)
        log_probs.append(log_prob)

        next_state, reward, done, truncated, _ = env.step(action.detach().numpy()[0])
        rewards.append(reward)
        state = next_state

        if truncated:
            done = True

    return log_probs, rewards


def compute_returns(rewards, gamma=0.99):
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    return returns


def update_policy(log_probs, returns, optimizer):
    loss = 0
    for log_prob, G in zip(log_probs, returns):
        loss += -log_prob * G
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()


def main():
    env = gym.make("MountainCarContinuous-v0")
    policy_net = ContinuousPolicyNet(state_dim=2, hidden_dim=64, action_dim=1)
    optimizer = optim.Adam(policy_net.parameters(), lr=3e-4)

    gamma = 0.99
    num_episodes = 500

    for i in range(num_episodes):
        log_probs, rewards = run_episode(env, policy_net)
        returns = compute_returns(rewards, gamma)
        loss_val = update_policy(log_probs, returns, optimizer)

        if (i + 1) % 20 == 0:
            print(
                f"Episode {i+1}/{num_episodes}, Return: {sum(rewards)}, Loss: {loss_val:.3f}"
            )

    env.close()


if __name__ == "__main__":
    main()
