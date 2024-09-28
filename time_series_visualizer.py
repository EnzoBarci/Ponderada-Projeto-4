import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importa os dados (Certifique-se de que as datas sejam analisadas. Considere definir a coluna do índice como 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Limpa os dados
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]  

def draw_line_plot():
    # Desenha o gráfico de linha
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], 'r', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Salva a imagem e retorna a figura (não mude esta parte)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copia e modifica os dados para o gráfico de barras mensais
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                    'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months_order, ordered=True)
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    df_bar = df_bar.reindex(months_order, axis=1)

    # Desenha o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(15, 5)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=months_order)

    # Salva a imagem e retorna a figura (não mude esta parte)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepara os dados para os gráficos de caixa (esta parte já está feita!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Desenha os gráficos de caixa (usando Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0]).set(title='Year-wise Box Plot (Trend)')
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).set(title='Month-wise Box Plot (Seasonality)')

    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Salva a imagem e retorna a figura (não mude esta parte)
    fig.savefig('box_plot.png')
    return fig
