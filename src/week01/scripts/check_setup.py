from src.utils import get_chain_context


if __name__ == "__main__":
    context = get_chain_context()
    print("Last block slot:", context.last_block_slot)
