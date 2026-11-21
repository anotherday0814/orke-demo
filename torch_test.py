import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)
print("CPU threads:", torch.get_num_threads())

# autograd: y = x^3 + 2x  ->  dy/dx = 3x^2 + 2
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3 + 2 * x
y.backward()
print("autograd dy/dx of x^3 + 2x at x=2:", x.grad.item(), "(expected 14.0)")

# Small linear regression: y = 3x + 1 + noise
torch.manual_seed(0)
X = torch.rand(100, 1, device=device) * 10
Y = 3 * X + 1 + 0.5 * torch.randn(100, 1, device=device)

model = torch.nn.Linear(1, 1).to(device)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
loss_fn = torch.nn.MSELoss()

for epoch in range(1, 1001):
    optimizer.zero_grad()
    loss = loss_fn(model(X), Y)
    loss.backward()
    optimizer.step()
    if epoch in (1, 250, 500, 1000):
        print(f"epoch {epoch:4d}  loss {loss.item():.4f}")

w = model.weight.item()
b = model.bias.item()
print(f"learned: y = {w:.3f}x + {b:.3f}  (true: y = 3x + 1)")
