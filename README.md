# Django e-commerce opensource
## Made with django + tailwindcss + daisyUI + docker
There is some function are not finished yet but if you know how to improve it. Just make a Pull <3

Origin template of fajar7xx: [link](https://github.com/fajar7xx/ecommerce-template-tailwind-1)

## Run with Podman

This repository includes `podman-compose.yml` so you can run the stack with Podman.

### Requirements

- Podman 4+
- Compose provider (`podman compose`) or `podman-compose`

### Start services (Podman)

1. Start database:

	```bash
	podman compose -f podman-compose.yml up -d db
	```

2. Build Tailwind/CSS assets:

	```bash
	podman compose -f podman-compose.yml run --rm saleapp_build_res
	```

3. Run migrations:

	```bash
	podman compose -f podman-compose.yml run --rm saleapp_migration
	```

4. Start Django app:

	```bash
	podman compose -f podman-compose.yml up saleapp
	```

5. Stop everything:

	```bash
	podman compose -f podman-compose.yml down
	```

If your system uses `podman-compose` (hyphenated), replace `podman compose` with `podman-compose` in the commands above.
