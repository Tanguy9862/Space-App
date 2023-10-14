import plotly.express as px


# FIGURE:
def create_choropleth_chart(df_launches_per_country):
    fig = px.choropleth(
        df_launches_per_country,
        locations='country_code',
        color='Total Number of Launches',
        color_continuous_scale=px.colors.sequential.haline_r[8:],
        custom_data=['Country', 'country_code']
    )

    fig.update_geos(
        projection_type='orthographic',
        projection_rotation_lon=-170,  # 110
        projection_rotation_lat=20,
        showocean=False,
        showcoastlines=True,
        coastlinecolor='white',
        coastlinewidth=1,
        showland=False,
        landcolor='#07053E',  # couleur continent
        showlakes=False,
        lakecolor='#202E78',  # couleur lac
        showcountries=False,
        countrycolor='white',
        bgcolor='rgba(0,0,0,0)',
        framewidth=1,
        framecolor='white',  # couleur du contour
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        coloraxis_showscale=False,
        hoverlabel=dict(
            bgcolor='rgba(11, 6, 81, 0.8)',
            bordercolor='rgba(11, 6, 81, 0.8)',
            font=dict(
                color='white'
            )
        )
    )

    fig.update_traces(
        marker_line_width=1,
        marker_line_color='white',
        hovertemplate=(
                '<b>%{customdata[0]} (%{customdata[1]})</b><br>' +
                'Total number of Rockets launched: %{z}<br>'
        )
    )

    return fig

