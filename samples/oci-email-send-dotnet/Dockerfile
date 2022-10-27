FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add SendEmail.csproj
RUN dotnet build SendEmail.csproj -c Release
RUN dotnet publish SendEmail.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "SendEmail.dll"]
CMD ["SendEmail:Function:function_handler"]