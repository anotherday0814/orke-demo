import jax
import jax.numpy as jnp

print("JAX version:", jax.__version__)
print("Default backend:", jax.default_backend())
print("Devices:", jax.devices())

# jax.grad: f(x) = x^3 + 2x  ->  f'(x) = 3x^2 + 2
def f(x):
    return x ** 3 + 2.0 * x

df = jax.grad(f)
print("grad of x^3 + 2x at x=2.0:", df(2.0), "(expected 14.0)")

# jax.jit: compiled function
@jax.jit
def selu(x, alpha=1.67, lam=1.05):
    return lam * jnp.where(x > 0, x, alpha * jnp.exp(x) - alpha)

x = jnp.arange(-2.0, 3.0)
print("jit selu input: ", x)
print("jit selu output:", selu(x))

# grad + jit together
fast_df = jax.jit(jax.grad(f))
print("jit(grad(f)) at x=3.0:", fast_df(3.0), "(expected 29.0)")
