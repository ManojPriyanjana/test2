async function fetchProducts() {
  const res = await fetch('/products');
  const products = await res.json();
  const list = document.getElementById('products');
  products.forEach(p => {
    const li = document.createElement('li');
    li.innerHTML = `${p.name} - $${p.price.toFixed(2)} <button onclick="addToCart(${p.id}, '${p.name}', ${p.price})">Add</button>`;
    list.appendChild(li);
  });
}

const cart = [];

function addToCart(id, name, price) {
  const item = cart.find(i => i.id === id);
  if (item) {
    item.quantity += 1;
  } else {
    cart.push({id, name, price, quantity:1});
  }
  renderCart();
}

function renderCart() {
  const list = document.getElementById('cart');
  list.innerHTML = '';
  let total = 0;
  cart.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.name} x${item.quantity}`;
    list.appendChild(li);
    total += item.price * item.quantity;
  });
  document.getElementById('total').textContent = total.toFixed(2);
}

async function checkout() {
  const res = await fetch('/checkout', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({items: cart.map(i => ({id: i.id, quantity: i.quantity}))})
  });
  const data = await res.json();
  alert('Total: $' + data.total.toFixed(2));
  cart.length = 0;
  renderCart();
}

fetchProducts();
