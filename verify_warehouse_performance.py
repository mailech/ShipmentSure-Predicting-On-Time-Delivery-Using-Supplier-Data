import pandas as pd

df = pd.read_csv("Train.csv")
pivot_table = df.pivot_table(values='Reached.on.Time_Y.N',
                           index='Warehouse_block',
                           columns='Mode_of_Shipment',
                           aggfunc='mean')

print("Warehouse Delivery Performance Pivot Table:")
print(pivot_table)

print("\nSpecific checks for D and F:")
for block in ['D', 'F']:
    print(f"\nWarehouse Block {block}:")
    block_data = df[df['Warehouse_block'] == block]
    for mode in df['Mode_of_Shipment'].unique():
        mode_data = block_data[block_data['Mode_of_Shipment'] == mode]
        mean_val = mode_data['Reached.on.Time_Y.N'].mean()
        print(f"  Mode {mode}: {mean_val:.4f}")
